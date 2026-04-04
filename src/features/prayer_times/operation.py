from typing import Protocol
from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.core.db.filters import Filter, Operator
from src.features.prayer_times.models.adapter import PrayerTimesAdapter
from src.features.prayer_times.models.schemas import (
    PrayerTimes,
    PrayerTimesCreate,
    PrayerTimesFilter,
)
from src.features.prayer_times.models.tables import PrayerTimesTable


class PrayerTimesOperationInterface(Protocol):
    def save(self, prayer_times_create: list[PrayerTimesCreate]): ...
    def find(self, mosque_id: str, filters: PrayerTimesFilter) -> list[PrayerTimes]: ...


class PrayerTimesOperation(PrayerTimesOperationInterface):
    def __init__(
        self,
        db_repository_provider: DatabaseRepositoryProvider,
    ):
        self.__db_repository = db_repository_provider
        self.__prayer_times_adapter = PrayerTimesAdapter()

    def save(self, prayer_times_create: list[PrayerTimesCreate]):
        with self.__db_repository.get_database_repository() as db:
            records = [
                db.create(self.__prayer_times_adapter.from_prayer_create(pt))
                for pt in prayer_times_create
            ]
            return self.__prayer_times_adapter.to_prayer_times_list(records)

    def find(self, mosque_id: str, filters: PrayerTimesFilter):
        with self.__db_repository.get_database_repository() as db:
            filters: list[Filter] = self.__get_filters(filters)
            filters.append(
                Filter(attribute="mosque_id", operator=Operator.EQ, value=mosque_id)
            )
            records = db.get_all(
                model=PrayerTimesTable,
                filters=filters,
            )
            return self.__prayer_times_adapter.to_prayer_times_list(records)

    def __get_filters(self, filters_params: PrayerTimesFilter) -> list[Filter]:
        filters: list[Filter] = Filter.get_validity_filters(filters_params.valid_at)
        if filters_params.year:
            filters.append(
                Filter(
                    attribute="year", operator=Operator.EQ, value=filters_params.year
                )
            )
        if filters_params.month:
            filters.append(
                Filter(
                    attribute="month", operator=Operator.EQ, value=filters_params.month
                )
            )
            if filters_params.day:
                filters.append(
                    Filter(
                        attribute="day", operator=Operator.EQ, value=filters_params.day
                    )
                )
        return filters
