import contextlib
from typing import Any, Generator

from sqlmodel import Session

from src.data_layer.db.database_connection import DatabaseConnection
from src.data_layer.db.database_repository import DatabaseRepository
from src.logger.logger import logger


class DatabaseRepositoryProvider:
    def __init__(self, database_connection: DatabaseConnection):
        self.__database_connection = database_connection

    @contextlib.contextmanager
    def get_database_repository(self) -> Generator[DatabaseRepository, Any, None]:
        logger.debug("Open DB session")
        with Session(self.__database_connection.get_engine()) as session:
            yield DatabaseRepository(session)
        logger.debug("Close DB session")
