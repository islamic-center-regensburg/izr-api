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
    PrayerTimesIn,
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

    def save_prayer_times_rows(
        self, mosque_id: int, upload_id: int, rows: list[PrayerTimesIn]
    ):
        with self.__db_repository.get_database_repository() as db:
            for row in rows:
                db.create(
                    PrayerTimesTable(
                        fajr=row.fajr,
                        shuruq=row.shuruq,
                        dhuhr=row.dhuhr,
                        asr=row.asr,
                        maghrib=row.maghrib,
                        isha=row.isha,
                        gregorian_date=row.gregorian_date,
                        hijri_date=row.hijri_date,
                        year=int(row.gregorian_date.split("-")[2]),
                        month=int(row.gregorian_date.split("-")[1]),
                        day=int(row.gregorian_date.split("-")[0]),
                        mosque_id=mosque_id,
                        upload_id=upload_id,
                    )
                )

    def get_stored_prayer_times(self, mosque_id: int, filters: PrayerTimesFilter):
        filters = [
            Filter(attribute="mosque_id", operator=Operator.EQ, value=mosque_id),
            Filter(attribute="year", operator=Operator.EQ, value=filters.year),
            Filter(attribute="month", operator=Operator.EQ, value=filters.month),
            Filter(attribute="day", operator=Operator.EQ, value=filters.day),
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
