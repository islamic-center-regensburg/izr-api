import json
from pathlib import Path
from pydantic import BaseModel, ValidationError

from seed import seed_mosques, seed_prayer_configs

from src.core.logging.logger import logger
from src.core.dependencies import db_connection
from src.features.mosque.schemas import MosqueOut
from src.features.prayer_config.schemas import PrayerConfigurationOut
from src.core.db.database_repository_provider import DatabaseRepositoryProvider


class SeedData(BaseModel):
    mosques: list[MosqueOut]
    prayer_configs: list[PrayerConfigurationOut]


def load():
    data_file = Path(__file__).parent / "data.json"
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
            db_connection
        )

        seed_mosques.seed(data.mosques, db_repository_provider)
        seed_prayer_configs.seed(data.prayer_configs, db_repository_provider)
        logger.info("==> Data Seeding done")
    except Exception as e:
        logger.error("Error while seeding data !", e)
        exit(-1)


if __name__ == "__main__":
    main()
