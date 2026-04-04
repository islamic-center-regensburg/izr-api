from __future__ import annotations

from typing import Any, Callable
from uuid import UUID

from src.core.db.schemas import PaginationBuilder
from src.features.post.schemas import MediaOut, PostListOut
from src.features.post.schemas import PostOut, PostTranslationOut


class PostAdapter:
    @staticmethod
    def _to_post_translations_out(
        post: Any,
        get_media_in_directory: Callable[[UUID, str], list[MediaOut]],
    ) -> list[PostTranslationOut]:
        return [
            PostTranslationOut(
                id=translation.id,
                title=translation.title,
                description=translation.description,
                language=translation.language,
                media=(
                    get_media_in_directory(post.mosque_id, translation.media)
                    if translation.media
                    else None
                ),
            )
            for translation in post.translations
        ]

    @staticmethod
    def to_post_out(
        post: Any,
        get_media_in_directory: Callable[[UUID, str], list[MediaOut]],
    ) -> PostOut:
        return PostOut(
            id=post.id,
            mosque_id=post.mosque_id,
            content_type=post.content_type,
            created_at=post.created_at,
            updated_at=post.updated_at,
            valid_to=post.valid_to,
            translations=PostAdapter._to_post_translations_out(
                post, get_media_in_directory
            ),
        )

    @staticmethod
    def to_post_list_out(
        posts: PostListOut,
        get_media_in_directory: Callable[[UUID, str], list[MediaOut]],
    ) -> PostListOut:
        mapped_posts = [
            PostAdapter.to_post_out(
                post=post,
                get_media_in_directory=get_media_in_directory,
            )
            for post in posts.data
        ]

        return PaginationBuilder.build(
            items=mapped_posts,
            total=posts.metadata.total,
            page=posts.metadata.page,
            size=posts.metadata.size,
        )
