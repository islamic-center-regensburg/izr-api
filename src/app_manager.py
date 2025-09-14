import contextlib
import logging
from src.logger.logger import logger

from fastapi import FastAPI
from pydantic import Field
from pydantic_settings import BaseSettings
from starlette.middleware.cors import CORSMiddleware

from src.data_layer.db.database_connection import DatabaseConnection
from src.data_layer.db.database_repository_provider import DatabaseRepositoryProvider
from src.data_layer.db.database_settings import DatabaseSettings


class AppManagerSettings(BaseSettings):
    version: str = Field(default="0.0.0", alias="APP_VERSION")
    title: str = Field(default="IZR API", alias="APP_TITLE")


class AppManager:
    def __init__(
        self,
        app_manager_settings: AppManagerSettings | None = None,
        db_connection: DatabaseConnection | None = None,
    ):
        app_manager_settings = app_manager_settings or AppManagerSettings()
        db_connection = db_connection or DatabaseConnection(
            database_settings=DatabaseSettings()
        )

        self.__app = FastAPI(
            title=app_manager_settings.title,
            version=app_manager_settings.version,
            lifespan=self.__lifespan,
        )
        # self.__app_manager_settings = app_manager_settings
        # self.__cors_settings = app_manager_settings.cors_settings

        self.__database_repository_provider = DatabaseRepositoryProvider(db_connection)

    @contextlib.asynccontextmanager
    async def __lifespan(self, app: FastAPI):
        self.__init_logger()
        self.__upgrade_database()
        yield

    def get_fast_api_app(self) -> FastAPI:
        # self.__add_middlewares()
        self.__add_routers()
        return self.__app

    @staticmethod
    def __upgrade_database():
        from alembic.command import upgrade
        from alembic.config import Config

        alembic_config = Config("alembic.ini")
        try:
            upgrade(config=alembic_config, revision="head")
        except Exception as e:
            logger.error("Error while upgrading database", exc_info=True)
            msg = "Database migration failed. Aborting startup."
            raise RuntimeError(msg) from e

    @staticmethod
    def __init_logger():
        logger = logging.getLogger("uvicorn.access")
        handler = logging.FileHandler(filename="api.log", mode="a")

        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

    def __add_routers(self):
        for controller in [
            # add controllers here
        ]:
            self.__app.include_router(controller.get_router())

    def __add_middlewares(self):
        logger.info(f"Allowed origins: {self.__cors_settings.frontend_url}")
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=[self.__cors_settings.frontend_url],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        )
