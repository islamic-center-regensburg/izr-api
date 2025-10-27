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
                latitude_adjustment_method=config_data.latitude_adjustment_method,
                midnight_mode=config_data.midnight_mode,
                shafaq=config_data.shafaq,
                calendar_method=config_data.calendar_method,
            )
            db.create(prayer_time_config)
            return prayer_time_config
