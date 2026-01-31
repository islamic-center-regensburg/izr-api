from src.features.mosque.schemas import MosqueIn, MosqueFilter
from src.features.mosque.operation import MosqueOperation


class MosqueComponent:
    def __init__(
        self,
        mosque_operation: MosqueOperation,
    ):
        self.mosque_operation = mosque_operation

    def get_all_mosques(self, filter: MosqueFilter):
        mosques = self.mosque_operation.get_all_mosques(filter)
        return mosques

    def get_mosque_by_id(self, mosque_id: int):
        mosque = self.mosque_operation.get_mosque_by_id(mosque_id)
        return mosque

    def add_mosque(self, mosque_data: MosqueIn):
        mosque = self.mosque_operation.add_mosque(mosque_data)
        return mosque
