from uuid import UUID
from src.features.mosque.adapter import MosqueAdapter
from src.features.mosque.operation import MosqueOperationInterface
from src.features.mosque.models.schemas import (
    MosqueCreate,
    MosqueQueryParams,
    MosqueUpdate,
)
from src.features.prayer_config.operation import PrayerConfigOperation


class MosqueComponent:
    def __init__(
        self,
        mosque_operation: MosqueOperationInterface,
        prayer_config_operation: PrayerConfigOperation,
    ):
        self.__mosque_operation = mosque_operation
        self.__prayer_config_operation = prayer_config_operation
        self.__mosque_adapter = MosqueAdapter()

    def get_all_mosques(self, query: MosqueQueryParams):
        return self.__mosque_adapter.to_mosques_read(
            self.__mosque_operation.find(query)
        )

    def get_mosque_by_id(self, mosque_id: UUID):
        return self.__mosque_adapter.to_mosque_read(
            self.__mosque_operation.get(mosque_id)
        )

    def add_mosque(self, mosque_data: MosqueCreate):
        return self.__mosque_operation.create(mosque_data)

    def update_mosque(self, mosque_id: UUID, mosque_data: MosqueUpdate):
        if mosque_data.prayer_config_id is not None:
            prayer_config = self.__prayer_config_operation.get_by_id(
                mosque_data.prayer_config_id
            )
            if prayer_config is None:
                raise ValueError("Invalid prayer_config_id")

        mosque = self.__mosque_operation.update(mosque_id, mosque_data)
        return mosque
