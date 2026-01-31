from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.mosque.schemas import MosqueIn
from src.features.mosque.operation import MosqueOperation
from src.core.logging.logger import logger


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

    logger.info("--> Seeded Mosques")
