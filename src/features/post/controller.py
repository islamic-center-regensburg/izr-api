from uuid import UUID
from fastapi import APIRouter, Body, Depends

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
        mosque_id: UUID,
        post_id: UUID,
        post_translation_in: PostTranslationIn = Depends(),
        description: str | None = Body(
            None, description="Description of the post translation"
        ),
        minio_repository_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> PostTranslationRead:
        return await self.__post_component.create_post_translation(
            mosque_id,
            post_id,
            post_translation_in,
            description,
            minio_repository_provider,
        )
