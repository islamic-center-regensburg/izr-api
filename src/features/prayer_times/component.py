from src.features.mosque.operation import MosqueOperation
from src.features.prayer_config.operation import PrayerConfigOperation
from src.features.prayer_times.integration import (
    AlAdhanAPIClientProvider,
    AlAdhanPrayerTimesParams,
)
from src.features.prayer_times.models.adapter import (
    AlAdhanPrayerTimesParamsAdapter,
    PrayerTimesAdapter,
)
from src.features.prayer_times.models.schemas import (
    AlAdhanPrayerTimesFilter,
    PrayerTimesFilter,
)
from src.features.prayer_times.operation import PrayerTimesOperation
from src.features.prayer_times.enums import PrayerTimesSource


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
        self.__prayer_times_adapter = PrayerTimesAdapter()
        self.__al_adhan_client_provider = AlAdhanAPIClientProvider()
        self.__al_adhan_params_adapter = AlAdhanPrayerTimesParamsAdapter()

    def __get_stored_prayer_times(
        self,
        mosque_id: str,
        filters: PrayerTimesFilter,
    ):
        return self.__prayer_times_operation.find(mosque_id, filters)

    def get_prayer_times_for_mosque(
        self,
        mosque_id: str,
        filters: PrayerTimesFilter,
    ):
        if filters.source == PrayerTimesSource.STORED:
            return self.__get_stored_prayer_times(mosque_id, filters)
        else:
            mosque = self.__mosque_operation.get(mosque_id)
            cfg = self.__prayer_config_operation.get_by_id(mosque.prayer_config_id)
            if not cfg:
                raise ValueError("No prayer configuration found for the mosque")

            prayer_times = self.__fetch_prayer_times(
                self.__al_adhan_params_adapter.from_prayer_times_filter_and_mosque(
                    filters, mosque, cfg
                )
            )

            return self.__prayer_times_adapter.to_prayer_times_list(prayer_times)

    def get_prayer_times(
        self,
        filters: AlAdhanPrayerTimesFilter,
    ):
        prayer_times = self.__fetch_prayer_times(
            self.__al_adhan_params_adapter.from_al_adhan_prayer_times_filter(filters)
        )
        return self.__prayer_times_adapter.to_prayer_times_list(prayer_times)

    def __fetch_prayer_times(self, params: AlAdhanPrayerTimesParams):
        response = self.__al_adhan_client_provider.get_prayer_times(params)
        if response.code != 200:
            raise ValueError(
                f"Invalid response from AlAdhan API: expected code 200, got {response.code}"
            )
        return self.__prayer_times_adapter.from_adhan_api(response)
