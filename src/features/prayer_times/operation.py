from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.core.db.filters import Filter, Operator
from src.features.mosque.schemas import Mosque
from src.features.prayer_config.schemas import (
    PrayerConfiguration,
)
from src.features.prayer_times.adapter import (
    AlAdhanPrayerTimesAdapter,
)
from src.features.prayer_times.repository import AlAdhanAPIClientProvider
from src.features.prayer_times.schemas import (
    PrayerTimesFilter,
    PrayerTimesTable,
    PrayerTimesTimingsParams,
)


class PrayerTimesOperation:
    def __init__(
        self,
        db_repository_provider: DatabaseRepositoryProvider,
    ):
        self.__db_repository = db_repository_provider
        self.__aladhan_api_client_provider = AlAdhanAPIClientProvider()
        self.__aladhan_prayer_times_adapter = AlAdhanPrayerTimesAdapter()

    def get_stored_prayer_times(self, mosque_id: int, filters: PrayerTimesFilter):
        filters = [
            Filter(attribute="mosque_id", operator=Operator.EQ, value=mosque_id),
            Filter(attribute="year", operator=Operator.EQ, value=filters.year),
            Filter(attribute="month", operator=Operator.EQ, value=filters.month),
            Filter(attribute="gregorian_date", operator=Operator.EQ, value=filters.day),
        ]
        with self.__db_repository.get_database_repository() as db:
            items = db.get_all(PrayerTimesTable, filters=filters)
            return items

    def fetch_prayer_times_for_mosque(
        self,
        prayer_config: PrayerConfiguration,
        mosque: Mosque,
        filters: PrayerTimesFilter,
    ):
        return self.__aladhan_prayer_times_adapter.toPrayerTimesOut(
            self.__aladhan_api_client_provider.get_timings(
                config=prayer_config, mosque=mosque, filters=filters
            )
        )

    def fetch_prayer_times(self, params: PrayerTimesTimingsParams):
        func = (
            self.__aladhan_api_client_provider.get_timings
            if params.day
            else self.__aladhan_api_client_provider.get_calendar
        )

        return self.__aladhan_prayer_times_adapter.toPrayerTimesOut(func(params=params))
