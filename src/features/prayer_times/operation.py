import aladhan
from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.core.db.filters import Filter, Operator
from src.features.prayer_config.schemas import (
    PrayerTimeConfigurationOut,
)
from src.features.prayer_times.adapter import (
    AlAdhanParametersAdapter,
    AlAdhanPrayerTimesAdapter,
)
from src.features.prayer_times.repository import AlAdhanAPIClientProvider
from src.features.prayer_times.schemas import (
    PrayerTimesFilter,
    PrayerTimesGenericParams,
    PrayerTimesTable,
)


class PrayerTimesOperation:
    def __init__(
        self,
        db_repository_provider: DatabaseRepositoryProvider,
    ):
        self.__db_repository = db_repository_provider
        self.__aladhan_api_client_provider = AlAdhanAPIClientProvider()
        self.__aladhan_params_adapter = AlAdhanParametersAdapter()

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
        prayer_config: PrayerTimeConfigurationOut,
        filters: PrayerTimesFilter,
    ):
        aladhan_params = self.__aladhan_params_adapter.toAlAdhanParameters(
            prayer_config
        )
        return self.__aladhan_api_client_provider.get_calendar(
            latitude=prayer_config.latitude,
            longitude=prayer_config.longitude,
            timezone=prayer_config.timezone,
            month=filters.month,
            year=filters.year,
            params=aladhan_params,
        )

    def fetch_prayer_times(
        self, filters: PrayerTimesFilter, params: PrayerTimesGenericParams
    ):
        if not filters.month and not filters.year and filters.day:
            raw = self.__aladhan_api_client_provider.get_timings(
                latitude=params.latitude,
                longitude=params.longitude,
                day=filters.day,
                params=aladhan.Parameters(
                    method=params.method, adjustment=params.hijri_adjustment
                ),
            )
            return AlAdhanPrayerTimesAdapter.adapt(raw)

        raw = self.__aladhan_api_client_provider.get_calendar(
            latitude=params.latitude,
            longitude=params.longitude,
            year=filters.year,
            month=filters.month,
            params=aladhan.Parameters(
                method=params.method, adjustment=params.hijri_adjustment
            ),
        )

        return AlAdhanPrayerTimesAdapter.adapt(raw)
