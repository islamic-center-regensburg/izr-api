from uuid import UUID
from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.core.db.filters import Filter, Operator
from src.core.db.pagination import PaginatedResponse, PaginationBuilder
from src.features.prayer_iqama.schemas import (
    PrayerIqamaFilter,
    PrayerIqamaIn,
    PrayerIqamaOut,
    PrayerIqamaTable,
    PrayerIqamaUpdate,
)


class PrayerIqamaOperation:
    def __init__(self, db_respository_provider: DatabaseRepositoryProvider):
        self.__db_respository_provider = db_respository_provider

    def get_all_prayer_iqamas(
        self, filter: PrayerIqamaFilter
    ) -> PaginatedResponse[PrayerIqamaOut]:
        filters = [
            Filter(
                attribute="prayer_name", operator=Operator.EQ, value=filter.prayer_name
            ),
            Filter(attribute="mode", operator=Operator.EQ, value=filter.mode),
            Filter(attribute="mosque_id", operator=Operator.EQ, value=filter.mosque_id),
        ]

        with self.__db_respository_provider.get_database_repository() as db:
            data = db.get_all(
                PrayerIqamaTable,
                filters=filters,
                limit=filter.limit,
                offset=filter.offset,
            )
            count = db.count(PrayerIqamaTable, filters=filters)
            return PaginationBuilder.build(
                items=data, total=count, page=filter.page, size=filter.size
            )

    def get_all_prayer_iqamas_for_mosque(self, mosque_id: UUID) -> list[PrayerIqamaOut]:
        filters = [
            Filter(attribute="mosque_id", value=mosque_id, operator=Operator.EQ),
        ]
        with self.__db_respository_provider.get_database_repository() as db:
            data = db.get_all(
                PrayerIqamaTable,
                filters=filters,
            )
            return data

    def create(self, prayer_iqama_in: PrayerIqamaIn) -> PrayerIqamaOut:
        with self.__db_respository_provider.get_database_repository() as db:
            prayer_iqama_record = PrayerIqamaTable(
                mosque_id=prayer_iqama_in.mosque_id,
                prayer_name=prayer_iqama_in.prayer_name,
                mode=prayer_iqama_in.mode,
                offset_minutes=prayer_iqama_in.offset_minutes,
                fixed_time=prayer_iqama_in.fixed_time,
            )
            prayer_iqama = db.create(prayer_iqama_record)
            return prayer_iqama

    def update(
        self,
        prayer_iqama_id: UUID,
        prayer_iqama_update: PrayerIqamaUpdate,
    ) -> PrayerIqamaOut:
        with self.__db_respository_provider.get_database_repository() as db:
            prayer_iqama = db.get_by_id(PrayerIqamaTable, id=prayer_iqama_id)
            if prayer_iqama is None:
                raise (
                    ValueError("Prayer Iqama not found")
                    if prayer_iqama is None
                    else None
                )

            if prayer_iqama_update.mode is not None:
                prayer_iqama.mode = prayer_iqama_update.mode
            if prayer_iqama_update.offset_minutes is not None:
                prayer_iqama.offset_minutes = prayer_iqama_update.offset_minutes
            if prayer_iqama_update.fixed_time is not None:
                prayer_iqama.fixed_time = prayer_iqama_update.fixed_time

            updated_prayer_iqama = db.update(prayer_iqama)
            return updated_prayer_iqama
