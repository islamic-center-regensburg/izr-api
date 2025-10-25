from src.data_layer.db.database_repository_provider import DatabaseRepositoryProvider
from src.data_layer.mosque.schema import MosqueTable


class MosqueOperation:
    def __init__(self, db_repository_provider: DatabaseRepositoryProvider):
        self.db_repository = db_repository_provider

    def get_mosque_by_id(self, mosque_id: str):
        with self.db_repository.get_database_repository() as db:
            mosque = db.get_by_id(MosqueTable, mosque_id)
            return mosque
