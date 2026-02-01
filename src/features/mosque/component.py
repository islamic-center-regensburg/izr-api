from src.features.mosque.schemas import MosqueIn, MosqueFilter, MosqueUpdate
from src.features.mosque.operation import MosqueOperation
from src.features.prayer_config.operation import PrayerConfigOperation


class MosqueComponent:
    def __init__(
        self,
        mosque_operation: MosqueOperation,
        prayer_config_operation: PrayerConfigOperation,
    ):
        self.mosque_operation = mosque_operation
        self.prayer_config_operation = prayer_config_operation

    def get_all_mosques(self, filter: MosqueFilter):
        mosques = self.mosque_operation.get_all_mosques(filter)
        return mosques

    def get_mosque_by_id(self, mosque_id: int):
        mosque = self.mosque_operation.get_mosque_by_id(mosque_id)
        return mosque

    def add_mosque(self, mosque_data: MosqueIn):
        mosque = self.mosque_operation.add_mosque(mosque_data)
        return mosque

    def update_mosque(self, mosque_id: int, mosque_data: MosqueUpdate):
        if mosque_data.prayer_config_id is not None:
            prayer_config = self.prayer_config_operation.get_by_id(
                mosque_data.prayer_config_id
            )
            if prayer_config is None:
                raise ValueError("Invalid prayer_config_id")

        mosque = self.mosque_operation.update_mosque(mosque_id, mosque_data)
        return mosque
