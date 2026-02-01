from src.features.prayer_config.schemas import (
    PrayerConfigurationFilter,
    PrayerConfigurationIn,
)
from src.features.mosque.operation import MosqueOperation
from src.features.prayer_config.operation import PrayerConfigOperation


class PrayerConfigComponent:
    def __init__(
        self,
        prayer_config_operation: PrayerConfigOperation,
        mosque_operation: MosqueOperation,
    ):
        self.prayer_config_operation = prayer_config_operation
        self.mosque_operation = mosque_operation

    def get_all_prayer_configurations(self, filter: PrayerConfigurationFilter):
        return self.prayer_config_operation.get_all_prayer_configurations(filter)

    def add_prayer_configuration(
        self, mosque_id: str, config_data: PrayerConfigurationIn
    ):
        prayer_config = self.prayer_config_operation.add_prayer_configuration(
            mosque_id, config_data
        )
        return prayer_config

    def update_prayer_configuration(
        self, prayer_config_id: str, config_data: PrayerConfigurationIn
    ):
        prayer_config = self.prayer_config_operation.update_prayer_configuration(
            prayer_config_id, config_data
        )
        return prayer_config
