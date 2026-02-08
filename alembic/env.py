from alembic import context
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlmodel import SQLModel

from src.features.event.schemas import (
    EventTable,
    EventTranslationTable,
)
from src.features.media.schemas import MediaTable
from src.features.mosque.schemas import MosqueTable
from src.features.prayer_config.schemas import PrayerConfigurationTable
from src.features.prayer_iqama.schemas import PrayerIqamaTable
from src.features.prayer_times.schemas import PrayerTimesTable
from src.features.prayer_times_upload.schemas import PrayerTimeUploadTable


class DatabaseMigration:
    def run(self):
        if context.is_offline_mode():
            self.__run_migrations_offline()
        else:
            self.__run_migrations_online()

    @staticmethod
    def __get_target_metadata() -> MetaData:
        for model in {
            MosqueTable,
            PrayerConfigurationTable,
            PrayerTimesTable,
            PrayerTimeUploadTable,
            PrayerIqamaTable,
            MediaTable,
            EventTable,
            EventTranslationTable,
        }:
            model()
        return SQLModel.metadata

    def __run_migrations_offline(self) -> None:
        url = context.config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=self.__get_target_metadata(),
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()

    def __run_migrations_online(self) -> None:
        from src.core.db.database_connection import DatabaseConnection
        from src.core.db.database_settings import DatabaseSettings

        connectable = DatabaseConnection(DatabaseSettings()).engine

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=self.__get_target_metadata()
            )

            with context.begin_transaction():
                context.run_migrations()


load_dotenv()
DatabaseMigration().run()
