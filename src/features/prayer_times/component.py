from uuid import UUID
from src.features.mosque.operation import MosqueOperation
from src.features.prayer_config.operation import PrayerConfigOperation
from src.features.prayer_times.operation import PrayerTimesOperation
from src.features.prayer_times.enums import PrayerTimesSource
from src.features.prayer_times.schemas import (
    PrayerTimesFilter,
    PrayerTimesSourceParams,
    PrayerTimesTimingsParams,
)


class PrayerTimesComponent:
    def __init__(
        self,
        prayer_times_operation: PrayerTimesOperation,
        mosque_operation: MosqueOperation,
        prayer_config_operation: PrayerConfigOperation,
    ):
        self.__prayer_times_operation = prayer_times_operation
        self.__mosque_operation = mosque_operation
        self.__prayer_config_operation = prayer_config_operation

    def get_prayer_times(
        self,
        params: PrayerTimesTimingsParams,
    ):
        return self.__prayer_times_operation.fetch_prayer_times(params=params)

    def get_prayer_times_for_mosque(
        self,
        mosque_id: UUID,
        source: PrayerTimesSourceParams,
        filters: PrayerTimesFilter,
    ):
        match source.source:
            case PrayerTimesSource.API:
                mosque = self.__mosque_operation.get_mosque_by_id(mosque_id)
                cfg = self.__prayer_config_operation.get_by_id(mosque.prayer_config_id)
                if not cfg:
                    raise ValueError("No prayer configuration found for the mosque")

                return self.__prayer_times_operation.fetch_prayer_times_for_mosque(
                    prayer_config=cfg, mosque=mosque, filters=filters
                )

            case PrayerTimesSource.STORED:
                return self.__prayer_times_operation.get_stored_prayer_times(
                    mosque_id, filters
                )
