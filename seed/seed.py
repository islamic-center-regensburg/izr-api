import json
from pathlib import Path

from pydantic import BaseModel, ValidationError
from seed import seed_mosques, seed_prayer_time_configurations
from src.controller_layer.mosque.model import MosqueIn
from src.controller_layer.prayer_time.model import PrayerTimeConfigurationIn
from src.data_layer.db.database_repository_provider import DatabaseRepositoryProvider
from src.logger.logger import logger
from src.dependencies import db_connection


class SeedData(BaseModel):
    mosques: list[MosqueIn]
    prayer_time_configurations: list[PrayerTimeConfigurationIn]


def load():
    data_file = Path(__file__).parent / 'data.json'
    data: SeedData | None = None
    with open(data_file, "r") as f:
        data = json.load(f)
    try:
        return SeedData(**data)
    except ValidationError as e:
        logger.error("Invalid seed data:")
        logger.error(e.json(indent=2))
        raise


def main():
    try:
        data = load()
        db_repository_provider: DatabaseRepositoryProvider = DatabaseRepositoryProvider(
            db_connection)

        mosques_ids = seed_mosques.seed(data.mosques, db_repository_provider)
        seed_prayer_time_configurations.seed(
            data.prayer_time_configurations, mosques_ids, db_repository_provider)
        logger.info("==> Data Seeding done")
    except Exception as e:
        logger.error('Error while seeding data !', e)
        exit(-1)


if __name__ == "__main__":
    main()
