from src.controller_layer.prayer_time.model import PrayerTimeConfigurationIn
from src.data_layer.db.database_repository_provider import DatabaseRepositoryProvider
from src.logger.logger import logger
from src.component_layer.prayer_time.component import PrayerTimeOperation


def seed(prayer_time_configurations: list[PrayerTimeConfigurationIn], mosques_ids: list[int], db_repository_provider: DatabaseRepositoryProvider):

    if len(mosques_ids) > 1 and len(mosques_ids) != len(prayer_time_configurations):
        logger.error(
            'Error: Mosques and Prayer Time Confgurations number  must be equtal otherwise provide only one mosque')
        raise
    prayer_time_operator = PrayerTimeOperation(db_repository_provider)
    for index, cfg in enumerate(prayer_time_configurations):
        prayer_time_operator.add_prayer_time_configuration(
            mosques_ids[index if len(mosques_ids) != 1 else 0], cfg)
    logger.info('--> Seeded Prayer Times Configurations')
