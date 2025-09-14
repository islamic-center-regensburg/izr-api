import os

from dotenv import load_dotenv
from pydantic import ValidationError

from src.data_layer.db.database_connection import DatabaseConnection
from src.data_layer.db.database_settings import DatabaseSettings, TestDatabaseSettings
from src.logger.logger import logger

load_dotenv()

if os.getenv("PYTEST_RUNNING") == "true":
    test_db_settings = TestDatabaseSettings()
    db_connection = DatabaseConnection(test_db_settings)
else:
    try:
        db_settings = DatabaseSettings()
        db_connection = DatabaseConnection(db_settings)
    except ValidationError as e:
        logger.error("Error while loading database settings", exc_info=e)
        msg = "Please execute scripts/setup_env.sh"
        raise Exception(msg) from e

create_db_and_tables = db_connection.create_db_and_tables
drop_tables = db_connection.drop_tables
get_repository = db_connection.get_repository
