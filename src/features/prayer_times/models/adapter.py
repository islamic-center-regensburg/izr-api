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
    APIPrayerTimes,
    APIPrayerTimesOut,
    AlAdhanPrayerTimesFilter,
    PrayerTimesBase,
    StoredPrayerTimes,
    StoredPrayerTimesCreate,
    PrayerTimesFilter,
    StoredPrayerTimesOut,
)
from src.features.prayer_times.models.tables import PrayerTimesTable


class PrayerTimesAdapter:
    @staticmethod
    def to_stored_prayer_times(prayer_times: PrayerTimesTable) -> StoredPrayerTimes:
        return StoredPrayerTimes(
            fajr=prayer_times.fajr,
            shuruq=prayer_times.shuruq,
            dhuhr=prayer_times.dhuhr,
            asr=prayer_times.asr,
            maghrib=prayer_times.maghrib,
            isha=prayer_times.isha,
            gregorian_date=prayer_times.gregorian_date,
            hijri_date=prayer_times.hijri_date,
            valid_from=prayer_times.valid_from,
            valid_to=prayer_times.valid_to,
            update_reason=prayer_times.update_reason,
        )

    def to_stored_prayer_times_out(
        self, prayer_times: StoredPrayerTimes
    ) -> StoredPrayerTimesOut:
        return StoredPrayerTimesOut(
            fajr=prayer_times.fajr,
            shuruq=prayer_times.shuruq,
            dhuhr=prayer_times.dhuhr,
            asr=prayer_times.asr,
            maghrib=prayer_times.maghrib,
            isha=prayer_times.isha,
            gregorian_date=prayer_times.gregorian_date,
            hijri_date=prayer_times.hijri_date,
            valid_from=prayer_times.valid_from,
            valid_to=prayer_times.valid_to,
            update_reason=prayer_times.update_reason,
        )

    def to_api_prayer_times_out(self, prayer_times: APIPrayerTimes):
        return APIPrayerTimesOut(
            fajr=prayer_times.fajr,
            shuruq=prayer_times.shuruq,
            dhuhr=prayer_times.dhuhr,
            asr=prayer_times.asr,
            maghrib=prayer_times.maghrib,
            isha=prayer_times.isha,
            gregorian_date=prayer_times.gregorian_date,
            hijri_date=prayer_times.hijri_date,
        )

    def from_stored_prayer_times_create(
        self, prayer_times_create: StoredPrayerTimesCreate
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
            year=int(prayer_times_create.gregorian_date.split("-")[2]),
            month=int(prayer_times_create.gregorian_date.split("-")[1]),
            day=int(prayer_times_create.gregorian_date.split("-")[0]),
        )

    def to_stored_prayer_times_create(
        self, prayer_times: PrayerTimesBase, mosque_id: str
    ) -> StoredPrayerTimesCreate:
        return StoredPrayerTimesCreate(
            fajr=prayer_times.fajr,
            shuruq=prayer_times.shuruq,
            dhuhr=prayer_times.dhuhr,
            asr=prayer_times.asr,
            maghrib=prayer_times.maghrib,
            isha=prayer_times.isha,
            gregorian_date=prayer_times.gregorian_date,
            hijri_date=prayer_times.hijri_date,
            mosque_id=mosque_id,
        )

    def from_adhan_api(
        self, adhan_prayer_times: AlAdhanResponse
    ) -> list[APIPrayerTimes]:
        def __convert_item(item: AlAdhanPrayerTimesItem) -> APIPrayerTimes:
            return APIPrayerTimes(
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
