from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.prayer_config.schemas import PrayerConfigurationIn
from src.features.prayer_config.operation import PrayerConfigOperation
from src.core.logging.logger import logger


def seed(
    prayer_time_configurations: list[PrayerConfigurationIn],
    db_repository_provider: DatabaseRepositoryProvider,
):
    prayer_time_operator = PrayerConfigOperation(db_repository_provider)
    for index, cfg in enumerate(prayer_time_configurations):
        prayer_time_operator.add_prayer_configuration(index + 1, cfg)
    logger.info("--> Seeded Prayer Times Configurations")
