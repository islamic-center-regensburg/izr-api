from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.prayer_config.schemas import PrayerTimeConfigurationIn
from src.features.prayer_config.operation import PrayerConfigOperation
from src.core.logging.logger import logger


def seed(
    prayer_time_configurations: list[PrayerTimeConfigurationIn],
    mosques_ids: list[int],
    db_repository_provider: DatabaseRepositoryProvider,
):
    if len(mosques_ids) > 1 and len(mosques_ids) != len(prayer_time_configurations):
        logger.error(
            "Error: Mosques and Prayer Time Confgurations number  must be equtal otherwise provide only one mosque"
        )
        raise
    prayer_time_operator = PrayerConfigOperation(db_repository_provider)
    for index, cfg in enumerate(prayer_time_configurations):
        prayer_time_operator.add_prayer_configuration(
            mosques_ids[index if len(mosques_ids) != 1 else 0], cfg
        )
    logger.info("--> Seeded Prayer Times Configurations")
