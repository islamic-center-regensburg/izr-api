from src.controller_layer.mosque.model import MosqueIn
from src.data_layer.mosque.operation import MosqueOperation


class MosqueComponent:
    def __init__(
        self,
        mosque_operation: MosqueOperation,
    ):
        self.mosque_operation = mosque_operation

    def add_mosque(self, mosque_data: MosqueIn):
        mosque = self.mosque_operation.add_mosque(mosque_data)
        return mosque
