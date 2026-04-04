from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.mosque.models import MosqueOut, MosqueTable
from src.core.logging.logger import logger


def seed(mosques: list[MosqueOut], db_repository_provider: DatabaseRepositoryProvider):
    with db_repository_provider.get_database_repository() as db:
        for mosque in mosques:
            db.create(
                MosqueTable(
                    id=mosque.id,
                    name=mosque.name,
                    address=mosque.address,
                    city=mosque.city,
                    country=mosque.country,
                    latitude=mosque.latitude,
                    longitude=mosque.longitude,
                    timezone=mosque.timezone,
                    prayer_config_id=mosque.prayer_config_id,
                )
            )

    logger.info("--> Seeded Mosques")
