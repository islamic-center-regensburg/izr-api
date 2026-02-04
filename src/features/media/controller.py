from fastapi import APIRouter, Depends

from src.core.db.pagination import PageParams, PaginatedResponse
from src.core.exceptions import guard
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.features.media.component import MediaComponent
from src.features.media.schemas import MediaIn, MediaFilter, MediaOut
from src.features.media.storage import get_minio_repository
from src.integrations.minio.repository import MinioStorageProvider


class MediaController:
    def __init__(self, media_component: MediaComponent):
        self.__media_component = media_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/media", ["Media"])

        router_builder.add_method(
            "",
            endpoint_type=EndpointType.LIST,
            endpoint=self.__list,
            response_model=PaginatedResponse[MediaOut],
            summary="List Media",
        )
        router_builder.add_method(
            "/{mosque_id}",
            endpoint_type=EndpointType.LIST,
            endpoint=self.__list_for_mosque,
            response_model=PaginatedResponse[MediaOut],
            summary="List Media for Mosque",
        )

        router_builder.add_method(
            "/{media_id}",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_by_id,
            response_model=MediaOut,
            summary="Get Media by ID",
        )

        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__create,
            response_model=MediaOut,
            summary="Create Media",
        )

        router_builder.add_method(
            "/{media_id}",
            endpoint_type=EndpointType.DELETE,
            endpoint=self.__delete,
            response_model=str,
            summary="Delete Media",
        )

        return router_builder.get_router()

    @guard
    def __list(
        self,
        filter: MediaFilter = Depends(),
        minio_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> PaginatedResponse[MediaOut]:
        return self.__media_component.get_all_media(filter, minio_provider)

    @guard
    def __list_for_mosque(
        self,
        mosque_id: int,
        page_params: PageParams = Depends(),
        minio_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> PaginatedResponse[MediaOut]:
        return self.__media_component.get_all_media_for_mosque(
            mosque_id, page_params, minio_provider
        )

    @guard
    def __get_by_id(
        self,
        media_id: int,
        minio_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> MediaOut:
        return self.__media_component.get_media_by_id(media_id, minio_provider)

    @guard
    async def __create(
        self,
        data: MediaIn = Depends(),
        minio_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> MediaOut:
        return await self.__media_component.create_media(data, minio_provider)

    @guard
    def __delete(
        self,
        media_id: int,
        minio_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> str:
        return self.__media_component.delete_media(media_id, minio_provider)
