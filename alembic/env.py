from alembic import context
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlmodel import SQLModel

from src.data_layer.mosque.schema import MosqueTable
from src.data_layer.prayer_time.schema import PrayerTimeConfigurationTable


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
            PrayerTimeConfigurationTable,
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
        from src.data_layer.db.database_connection import DatabaseConnection
        from src.data_layer.db.database_settings import DatabaseSettings

        connectable = DatabaseConnection(DatabaseSettings()).engine

        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=self.__get_target_metadata()
            )

            with context.begin_transaction():
                context.run_migrations()


load_dotenv()
DatabaseMigration().run()
