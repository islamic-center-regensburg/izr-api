from fastapi import APIRouter, Depends

from src.core.exceptions import guard
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.features.media.component import MediaComponent
from src.features.media.schemas import DirectoryQuery, MediaFilter, MediaOut
from src.features.media.storage import get_minio_repository
from src.integrations.minio.repository import MinioStorageProvider


class MediaController:
    def __init__(self, media_component: MediaComponent):
        self.__media_component = media_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/media", ["Media"])

        router_builder.add_method(
            "",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_media,
            response_model=list[MediaOut],
            summary="List all Media in Directory",
        )
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.DELETE,
            endpoint=self.__delete_media,
            response_model=str,
            summary="Delete all Media in Directory",
        )

        return router_builder.get_router()

    @guard
    def __get_media(
        self,
        query: DirectoryQuery = Depends(),
        filter: MediaFilter = Depends(),
        minio_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> list[MediaOut]:
        return self.__media_component.get_all_media_in_directory(
            query, filter, minio_provider
        )

    @guard
    def __delete_media(
        self,
        query: DirectoryQuery = Depends(),
        minio_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> str:
        self.__media_component.delete_all_media_in_directory(query, minio_provider)
        return "Done"
