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
