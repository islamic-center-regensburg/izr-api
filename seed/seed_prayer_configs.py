from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.prayer_config.schemas import (
    PrayerConfigurationOut,
    PrayerConfigurationTable,
)
from src.core.logging.logger import logger


def seed(
    prayer_time_configurations: list[PrayerConfigurationOut],
    db_repository_provider: DatabaseRepositoryProvider,
):
    with db_repository_provider.get_database_repository() as db:
        for cfg in prayer_time_configurations:
            db.create(
                PrayerConfigurationTable(
                    id=cfg.id,
                    mosque_id=cfg.mosque_id,
                    calculation_method=cfg.calculation_method,
                    school=cfg.school,
                    midnight_mode=cfg.midnight_mode,
                    latitude_adjustment_method=cfg.latitude_adjustment_method,
                    tune=cfg.tune,
                    imsak_tune=cfg.imsak_tune,
                    fajr_tune=cfg.fajr_tune,
                    sunrise_tune=cfg.sunrise_tune,
                    dhuhr_tune=cfg.dhuhr_tune,
                    asr_tune=cfg.asr_tune,
                    maghrib_tune=cfg.maghrib_tune,
                    isha_tune=cfg.isha_tune,
                    midnight_tune=cfg.midnight_tune,
                    fajr_angle=cfg.fajr_angle,
                    maghrib_angle=cfg.maghrib_angle,
                    isha_angle=cfg.isha_angle,
                    shafaq=cfg.shafaq,
                    calendar_method=cfg.calendar_method,
                )
            )
    logger.info("--> Seeded Prayer Times Configurations")
