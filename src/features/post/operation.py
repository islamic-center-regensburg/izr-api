from uuid import UUID
from src.core.db.database_repository import DoesNotExistInDatabaseException
from src.core.db.database_repository_provider import DatabaseRepositoryProvider

from src.core.db.filters import Filter, Operator
from src.core.db.pagination import PaginationBuilder
from src.features.post.schemas import (
    PostPaginationFilter,
    PostRead,
    PostTranslationMetaIn,
    PostTranslationUpdate,
)
from src.features.post.schemas import (
    PostFilter,
    PostCreate,
    PostListOut,
    PostOut,
    PostTable,
    PostTranslationRead,
    PostTranslationTable,
    SupportedLanguages,
)


class PostOperation:
    def __init__(self, db_repository_provider: DatabaseRepositoryProvider):
        self.__db_repository_provider = db_repository_provider

    def get_post_by_id(self, post_id: UUID, filter: PostFilter) -> PostOut:
        with self.__db_repository_provider.get_database_repository() as db:
            filters = [
                Filter(attribute="id", value=post_id, operator=Operator.EQ),
                Filter(
                    attribute="valid_to", value=filter.date_from, operator=Operator.LE
                ),
            ]
            if filter.content_type is not None:
                filters.append(
                    Filter(
                        attribute="content_type",
                        value=filter.content_type,
                        operator=Operator.EQ,
                    )
                )
            post_records: list[PostRead] = db.get_all(PostTable, filters=filters)
            post = post_records[0]

            return PostOut(
                id=post.id,
                mosque_id=post.mosque_id,
                content_type=post.content_type,
                created_at=post.created_at,
                updated_at=post.updated_at,
                valid_to=post.valid_to,
                translations=[],
            )

    def get_all_posts(
        self, mosque_id: UUID, filter: PostPaginationFilter
    ) -> PostListOut:
        with self.__db_repository_provider.get_database_repository() as db:
            posts = []

            filters = [
                Filter(attribute="mosque_id", value=mosque_id, operator=Operator.EQ),
                Filter(
                    attribute="valid_to", value=filter.date_from, operator=Operator.LE
                ),
            ]
            if filter.content_type is not None:
                filters.append(
                    Filter(
                        attribute="content_type",
                        value=filter.content_type,
                        operator=Operator.EQ,
                    )
                )
            post_records: list[PostRead] = db.get_all(PostTable, filters=filters)
            for post in post_records:
                posts.append(
                    PostOut(
                        id=post.id,
                        mosque_id=post.mosque_id,
                        content_type=post.content_type,
                        created_at=post.created_at,
                        updated_at=post.updated_at,
                        valid_to=post.valid_to,
                        translations=[],
                    )
                )
            return PaginationBuilder.build(
                items=posts, total=len(posts), size=filter.size, page=filter.page
            )

    def create(
        self,
        post_create: PostCreate,
    ) -> PostRead:
        with self.__db_repository_provider.get_database_repository() as db:
            post_record = db.create(
                PostTable(
                    mosque_id=post_create.mosque_id,
                    content_type=post_create.content_type,
                    valid_to=post_create.valid_to,
                )
            )

            return post_record

    def delete_post(self, post_id: UUID) -> None:
        with self.__db_repository_provider.get_database_repository() as db:
            db.delete(PostTable, post_id)


class PostTranslationOperation:
    def __init__(self, db_repository_provider: DatabaseRepositoryProvider):
        self.__db_repository_provider = db_repository_provider

    def get_post_translations(
        self,
        post_id: UUID,
        language: SupportedLanguages | None,
    ) -> list[PostTranslationRead]:
        with self.__db_repository_provider.get_database_repository() as db:
            filters = [
                Filter(attribute="post_id", value=post_id, operator=Operator.EQ),
                Filter(
                    attribute="language",
                    value=language,
                    operator=Operator.EQ,
                ),
            ]
            return db.get_all(PostTranslationTable, filters=filters)

    def create_post_translation(
        self,
        post_id: UUID,
        post_translation_in: PostTranslationMetaIn,
        description: str | None,
        storage_dir_path: str | None = None,
    ) -> PostTranslationRead:
        with self.__db_repository_provider.get_database_repository() as db:
            return db.create(
                PostTranslationTable(
                    post_id=post_id,
                    title=post_translation_in.title,
                    description=description,
                    language=post_translation_in.language,
                    media=storage_dir_path,
                )
            )

    def get_post_translation_by_id(
        self,
        translation_id: UUID,
    ) -> PostTranslationRead:
        with self.__db_repository_provider.get_database_repository() as db:
            return db.get_by_id(PostTranslationTable, translation_id)

    def update_post_translation(
        self,
        post_id: UUID,
        translation_id: UUID,
        post_translation_in: PostTranslationUpdate,
        description: str | None,
    ) -> PostTranslationRead:
        with self.__db_repository_provider.get_database_repository() as db:
            post_translation = db.get_by_id(PostTranslationTable, translation_id)
            if post_translation.post_id != post_id:
                raise DoesNotExistInDatabaseException(
                    "Post translation does not belong to the given post"
                )

            post_translation.title = post_translation_in.title
            post_translation.language = post_translation_in.language
            post_translation.description = description

            return db.update(post_translation)

    def delete_post_translation(
        self,
        post_id: UUID,
        translation_id: UUID,
    ) -> None:
        with self.__db_repository_provider.get_database_repository() as db:
            post_translation = db.get_by_id(PostTranslationTable, translation_id)
            if post_translation.post_id != post_id:
                raise DoesNotExistInDatabaseException(
                    "Post translation does not belong to the given post"
                )
            db.delete(PostTranslationTable, translation_id)

    def clear_post_translation_media(
        self,
        translation_id: UUID,
    ) -> PostTranslationRead:
        with self.__db_repository_provider.get_database_repository() as db:
            post_translation = db.get_by_id(PostTranslationTable, translation_id)
            post_translation.media = None
            return db.update(post_translation)

    def set_post_translation_media(
        self,
        translation_id: UUID,
        storage_dir_path: str,
    ) -> PostTranslationRead:
        with self.__db_repository_provider.get_database_repository() as db:
            post_translation = db.get_by_id(PostTranslationTable, translation_id)
            post_translation.media = storage_dir_path
            return db.update(post_translation)
