from src.controller_layer.prayer_time.model import PrayerTimeConfigurationIn
from src.data_layer.db.database_repository_provider import DatabaseRepositoryProvider
from src.data_layer.db.filters import Filter, Operator
from src.data_layer.prayer_time.schema import PrayerTimeConfigurationTable


class PrayerTimeOperation:
    def __init__(self, db_repository_provider: DatabaseRepositoryProvider):
        self.db_repository = db_repository_provider

    def get_prayer_time_configuration_by_mosque(self, mosque_id: str):
        with self.db_repository.get_database_repository() as db:
            config = db.get_last(
                PrayerTimeConfigurationTable,
                filters=[Filter("mosque_id", Operator.EQ, mosque_id)],
            )
            return config

    def add_prayer_time_configuration(
        self, mosque_id: str, config_data: PrayerTimeConfigurationIn
    ):
        with self.db_repository.get_database_repository() as db:
            prayer_time_config = PrayerTimeConfigurationTable(
                mosque_id=int(mosque_id),
                calculation_method=config_data.calculation_method,
                school=config_data.school,
                midnight_mode=config_data.midnight_mode,
                latitude_adjustment_method=config_data.latitude_adjustment_method,
                tune=config_data.tune,
                imsak_tune=config_data.imsak_tune,
                fajr_tune=config_data.fajr_tune,
                sunrise_tune=config_data.sunrise_tune,
                dhuhr_tune=config_data.dhuhr_tune,
                asr_tune=config_data.asr_tune,
                maghrib_tune=config_data.maghrib_tune,
                isha_tune=config_data.isha_tune,
                midnight_tune=config_data.midnight_tune,
                fajr_angle=config_data.fajr_angle,
                maghrib_angle=config_data.maghrib_angle,
                isha_angle=config_data.isha_angle,
                shafaq=config_data.shafaq,
                calendar_method=config_data.calendar_method,
            )
            db.create(prayer_time_config)
            return prayer_time_config
