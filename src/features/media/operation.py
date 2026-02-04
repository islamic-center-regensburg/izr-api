from src.core.db.pagination import PageParams, PaginatedResponse, PaginationBuilder
from src.core.db.filters import Filter, Operator
from src.core.db.database_repository_provider import DatabaseRepositoryProvider

from src.features.media.schemas import (
    MediaCreate,
    MediaFilter,
    MediaOut,
    MediaTable,
)


class MediaOperation:
    def __init__(self, db_repository_provider: DatabaseRepositoryProvider):
        self.__db_repository_provider = db_repository_provider

    def get_all_media(self, filter: MediaFilter) -> PaginatedResponse[MediaOut]:
        filters = [
            Filter(attribute="id", value=filter.id, operator=Operator.EQ),
            Filter(attribute="mosque_id", value=filter.mosque_id, operator=Operator.EQ),
        ]
        with self.__db_repository_provider.get_database_repository() as db:
            data = db.get_all(
                MediaTable,
                filters=filters,
                limit=filter.limit,
                offset=filter.offset,
            )
            total = db.count(MediaTable, filters=filters)
            return PaginationBuilder.build(
                items=data,
                total=total,
                page=filter.page,
                size=filter.size,
            )

    def get_media_by_id(self, media_id: int):
        with self.__db_repository_provider.get_database_repository() as db:
            return db.get_by_id(MediaTable, media_id)

    def get_all_media_for_mosque(
        self, mosque_id: int, page_params: PageParams
    ) -> PaginatedResponse[MediaTable]:
        filters = [
            Filter(attribute="mosque_id", value=mosque_id, operator=Operator.EQ),
        ]
        with self.__db_repository_provider.get_database_repository() as db:
            data = db.get_all(
                MediaTable,
                filters=filters,
                limit=page_params.limit,
                offset=page_params.offset,
            )
            total = db.count(MediaTable, filters=filters)
            return PaginationBuilder.build(
                items=data,
                total=total,
                page=page_params.page,
                size=page_params.size,
            )

    def create(self, media_create: MediaCreate) -> MediaOut:
        with self.__db_repository_provider.get_database_repository() as db:
            record = MediaTable(
                mosque_id=media_create.mosque_id,
                object_key=media_create.object_key,
                type=media_create.type,
            )

            return db.create(record)

    def delete(self, media_id: int):
        with self.__db_repository_provider.get_database_repository() as db:
            media = db.get_by_id(MediaTable, media_id)
            if media is None:
                return None
            object_key = media.object_key
            db.delete(MediaTable, media_id)
            return object_key
