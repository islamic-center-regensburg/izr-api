from src.data_layer.db.database_repository_provider import DatabaseRepositoryProvider
from src.data_layer.mosque.schema import MosqueTable
from src.dependencies import db_connection
from src.controller_layer.mosque.model import MosqueIn
from src.logger.logger import logger
from src.component_layer.mosque.component import MosqueOperation


def seed(mosques: list[MosqueIn], db_repository_provider: DatabaseRepositoryProvider):
    try:
        mosque_operation = MosqueOperation(db_repository_provider)
        ids: list[int] = []
        for record in mosques:
            mosque = mosque_operation.add_mosque(record)
            ids.append(mosque.id)
        return ids
    except Exception as e:
        logger.error("Error wihile seeding Mosques !", e)

    logger.info('--> Seeded Mosques')
