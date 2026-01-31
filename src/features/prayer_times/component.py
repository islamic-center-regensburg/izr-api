from src.features.mosque.operation import MosqueOperation
from src.features.prayer_config.operation import PrayerConfigOperation
from src.features.prayer_config.schemas import PrayerConfigurationFilter
from src.features.prayer_times.operation import PrayerTimesOperation
from src.features.prayer_times.enums import PrayerTimesSource
from src.features.prayer_times.schemas import (
    PrayerTimesFilter,
    PrayerTimesGenericParams,
    PrayerTimesSourceParams,
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
        params: PrayerTimesGenericParams,
        filters: PrayerTimesFilter,
    ):
        return self.__prayer_times_operation.fetch_prayer_times(
            params=params, filters=filters
        )

    def get_prayer_times_for_mosque(
        self,
        mosque_id: int,
        source: PrayerTimesSourceParams,
        filters: PrayerTimesFilter,
    ):
        match source.source:
            case PrayerTimesSource.API:
                prayer_cfg_filters = PrayerConfigurationFilter(mosque_id=mosque_id)
                cfg = self.__prayer_config_operation.get_all_prayer_configurations(
                    prayer_cfg_filters
                )
                if not cfg.data:
                    raise ValueError("No prayer configuration found for the mosque")

                mosque = self.__mosque_operation.get_mosque_by_id(mosque_id)
                return self.__prayer_times_operation.fetch_prayer_times_for_mosque(
                    mosque, cfg.data[0], filters
                )

            case PrayerTimesSource.STORED:
                return self.__prayer_times_operation.get_stored_prayer_times(
                    mosque_id, filters
                )
