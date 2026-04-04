from src.features.mosque.models.schemas import Mosque
from src.features.prayer_config.adapter import PrayerConfigurationAdapter
from src.features.prayer_config.schemas import PrayerConfiguration
from src.features.prayer_times.integration import (
    AlAdhanPrayerTimesItem,
    AlAdhanPrayerTimesParams,
    AlAdhanCalendarType,
    AlAdhanResponse,
)
from src.features.prayer_times.models.schemas import (
    AlAdhanPrayerTimesFilter,
    PrayerTimes,
    PrayerTimesCreate,
    PrayerTimesFilter,
    PrayerTimesOut,
)
from src.features.prayer_times.models.tables import PrayerTimesTable


class PrayerTimesAdapter:
    @staticmethod
    def to_prayer_times(prayer_times: PrayerTimesTable) -> PrayerTimes:
        return PrayerTimes(
            fajr=prayer_times.fajr,
            shuruq=prayer_times.shuruq,
            dhuhr=prayer_times.dhuhr,
            asr=prayer_times.asr,
            maghrib=prayer_times.maghrib,
            isha=prayer_times.isha,
            gregorian_date=prayer_times.gregorian_date,
            hijri_date=prayer_times.hijri_date,
        )

    def to_prayer_times_list(
        self, prayer_times_list: list[PrayerTimesTable]
    ) -> list[PrayerTimes]:
        return [self.to_prayer_times(pt) for pt in prayer_times_list]

    def to_prayer_times_out(self, prayer_times: list[PrayerTimes]):
        return [
            PrayerTimesOut(
                fajr=item.fajr,
                shuruq=item.shuruq,
                dhuhr=item.dhuhr,
                asr=item.asr,
                maghrib=item.maghrib,
                isha=item.isha,
                gregorian_date=item.gregorian_date,
                hijri_date=item.hijri_date,
            )
            for item in prayer_times
        ]

    def from_prayer_create(
        self, prayer_times_create: PrayerTimesCreate
    ) -> PrayerTimesTable:
        return PrayerTimesTable(
            fajr=prayer_times_create.fajr,
            shuruq=prayer_times_create.shuruq,
            dhuhr=prayer_times_create.dhuhr,
            asr=prayer_times_create.asr,
            maghrib=prayer_times_create.maghrib,
            isha=prayer_times_create.isha,
            gregorian_date=prayer_times_create.gregorian_date,
            hijri_date=prayer_times_create.hijri_date,
            mosque_id=prayer_times_create.mosque_id,
        )

    def from_adhan_api(self, adhan_prayer_times: AlAdhanResponse) -> list[PrayerTimes]:
        def __convert_item(item: AlAdhanPrayerTimesItem) -> PrayerTimes:
            return PrayerTimes(
                fajr=item.timings.Fajr,
                shuruq=item.timings.Sunrise,
                dhuhr=item.timings.Dhuhr,
                asr=item.timings.Asr,
                maghrib=item.timings.Maghrib,
                isha=item.timings.Isha,
                gregorian_date=item.date.gregorian.date,
                hijri_date=item.date.hijri.date,
            )

        return [__convert_item(item) for item in adhan_prayer_times.data]


class AlAdhanPrayerTimesParamsAdapter:
    def __init__(self):
        self.__prayer_config_adapter = PrayerConfigurationAdapter()

    def from_prayer_times_filter_and_mosque(
        self,
        filters: PrayerTimesFilter,
        mosque: Mosque,
        mosque_config: PrayerConfiguration,
    ) -> AlAdhanPrayerTimesParams:
        query_params = self.__prayer_config_adapter.to_al_adhan_query_params(
            mosque_config
        )
        query_params.latitude = mosque.latitude
        query_params.longitude = mosque.longitude
        query_params.timezone = mosque.timezone

        return AlAdhanPrayerTimesParams(
            calendar=self.__get_calendar_type(filters),
            year=filters.year,
            month=filters.month,
            day=filters.day,
            query_params=query_params,
        )

    def from_al_adhan_prayer_times_filter(
        self, filters: AlAdhanPrayerTimesFilter
    ) -> AlAdhanPrayerTimesParams:
        return AlAdhanPrayerTimesParams(
            calendar=self.__get_calendar_type(filters),
            year=filters.timings.year,
            month=filters.timings.month,
            day=filters.timings.day,
            query_params=filters.query_params,
        )

    def __get_calendar_type(
        self, filters: PrayerTimesFilter | PrayerTimesFilter
    ) -> AlAdhanCalendarType:
        if filters.month and not filters.day:
            return AlAdhanCalendarType.MONTHLY
        elif filters.month and filters.day:
            return AlAdhanCalendarType.DAILY
        elif not filters.month and filters.day:
            raise ValueError("Day cannot be provided without month")
        else:
            return AlAdhanCalendarType.ANNUAL
