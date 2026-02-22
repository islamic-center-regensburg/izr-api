from uuid import UUID
from fastapi import APIRouter, Body, Depends, Query

from src.core.exceptions import guard
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.features.post.component import PostComponent
from src.features.post.schemas import (
    PostCreate,
    PostFilter,
    PostListOut,
    PostOut,
    PostPaginationFilter,
    PostRead,
    PostTranslationIn,
    PostTranslationMediaIn,
    PostTranslationRead,
)
from src.features.post.storage import get_minio_repository
from src.integrations.minio.repository import MinioStorageProvider


class PostController:
    def __init__(self, post_component: PostComponent):
        self.__post_component = post_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/posts", ["Posts"])

        router_builder.add_method(
            "/all/{mosque_id}",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_all_posts,
            response_model=PostListOut,
            summary="Get posts for mosque",
        )
        router_builder.add_method(
            "/{post_id}",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_post,
            response_model=PostOut,
            summary="Get post by ID",
        )

        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__create_post,
            response_model=PostRead,
            summary="Create post",
        )
        router_builder.add_method(
            "/{post_id}/translations",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__create_translation_for_post,
            response_model=PostTranslationRead,
            summary="Create post translation",
        )
        router_builder.add_method(
            "/{post_id}/translations/{translation_id}",
            endpoint_type=EndpointType.UPDATE,
            endpoint=self.__update_translation_for_post,
            response_model=PostTranslationRead,
            summary="Update post translation",
        )
        router_builder.add_method(
            "/{post_id}/translations/{translation_id}",
            endpoint_type=EndpointType.DELETE,
            endpoint=self.__delete_translation_for_post,
            response_model=bool,
            summary="Delete post translation",
        )
        router_builder.add_method(
            "/media/{translation_id}",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__upload_post_media,
            response_model=PostTranslationRead,
            summary="Upload post translation media",
        )
        router_builder.add_method(
            "/media/{translation_id}",
            endpoint_type=EndpointType.DELETE,
            endpoint=self.__delete_post_media,
            response_model=PostTranslationRead,
            summary="Delete post translation media",
        )
        router_builder.add_method(
            "/{post_id}",
            endpoint_type=EndpointType.DELETE,
            endpoint=self.__delete_post,
            response_model=bool,
            summary="Delete post",
        )

        return router_builder.get_router()

    @guard
    def __get_post(
        self,
        post_id: UUID,
        filter: PostFilter = Depends(),
        minio_repository_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> PostOut:
        return self.__post_component.get_post(
            post_id, filter, minio_repository_provider
        )

    @guard
    def __get_all_posts(
        self,
        mosque_id: UUID,
        filters: PostPaginationFilter = Depends(),
        minio_repository_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> PostListOut:
        return self.__post_component.get_all_posts(
            mosque_id, filters, minio_repository_provider
        )

    @guard
    def __create_post(
        self,
        post_create: PostCreate = Depends(),
    ) -> PostRead:
        return self.__post_component.create_post(
            post_create,
        )

    @guard
    async def __create_translation_for_post(
        self,
        post_id: UUID,
        post_translation_in: PostTranslationIn = Depends(),
        description: str | None = Body(
            None, description="Description of the post translation"
        ),
    ) -> PostTranslationRead:
        return self.__post_component.create_post_translation(
            post_id,
            post_translation_in,
            description,
        )

    @guard
    async def __upload_post_media(
        self,
        translation_id: UUID,
        post_translation_media_in: PostTranslationMediaIn = Depends(),
        minio_repository_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> PostTranslationRead:
        return await self.__post_component.upload_post_media(
            translation_id,
            post_translation_media_in,
            minio_repository_provider,
        )

    @guard
    def __update_translation_for_post(
        self,
        post_id: UUID,
        translation_id: UUID,
        post_translation_in: PostTranslationIn = Depends(),
        description: str | None = Body(
            None, description="Description of the post translation"
        ),
    ) -> PostTranslationRead:
        return self.__post_component.update_post_translation(
            post_id,
            translation_id,
            post_translation_in,
            description,
        )

    @guard
    def __delete_translation_for_post(
        self,
        post_id: UUID,
        translation_id: UUID,
        minio_repository_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> bool:
        return self.__post_component.delete_post_translation(
            post_id,
            translation_id,
            minio_repository_provider,
        )

    @guard
    def __delete_post_media(
        self,
        translation_id: UUID,
        file_path: str | None = Query(
            None,
            description="Optional file path to delete from translation media directory",
        ),
        minio_repository_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> PostTranslationRead:
        return self.__post_component.delete_post_media(
            translation_id,
            file_path,
            minio_repository_provider,
        )

    @guard
    def __delete_post(
        self,
        post_id: UUID,
        minio_repository_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> bool:
        return self.__post_component.delete_post(
            post_id,
            minio_repository_provider,
        )
