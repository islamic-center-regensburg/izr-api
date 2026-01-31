from typing import Protocol, Generator

from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session

from src.core.db.database_repository import DatabaseRepository
from src.core.logging.logger import logger


class DatabaseSettingsInterface(Protocol):
    @property
    def database_url(self) -> str: ...
    @property
    def engine_properties(self) -> dict: ...
    @property
    def drop_all_tables_query(self) -> str: ...


class DatabaseConnection:
    def __init__(self, database_settings: DatabaseSettingsInterface):
        logger.info("Initialize db connection")
        self.engine = create_engine(
            database_settings.database_url, **database_settings.engine_properties
        )
        self.__drop_all_tables_query = database_settings.drop_all_tables_query

    def create_db_and_tables(self) -> None:
        logger.info("Create tables")
        SQLModel.metadata.create_all(self.engine, checkfirst=True)

    def drop_tables(self) -> None:
        logger.info("Drop tables")

        with self.engine.connect() as conn:
            conn.execute(text(self.__drop_all_tables_query))
            conn.commit()

    def get_repository(self) -> Generator[DatabaseRepository, None, None]:
        logger.debug("Open DB session")
        with Session(self.engine) as session:
            yield DatabaseRepository(session)
        logger.debug("Close DB session")

    def get_engine(self):
        return self.engine
