from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import StaticPool


class DatabaseSettings(BaseSettings):
    db_username: str = Field(default=..., alias="DB_ADMIN_USERNAME")
    db_password: str = Field(default=..., alias="DB_ADMIN_PASSWORD")
    db_server: str = Field(default=..., alias="DB_SERVER")
    db_name: str = Field(default=..., alias="DB_NAME")
    db_port: int = Field(default=..., alias="DB_PORT")

    @property
    def database_url(self) -> str:
        return "postgresql://{0}:{1}@{2}:{3}/{4}".format(
            self.db_username,
            self.db_password,
            self.db_server,
            self.db_port,
            self.db_name,
        )

    @property
    def engine_properties(self) -> dict:
        return dict(pool_size=10, max_overflow=20)

    @property
    def drop_all_tables_query(self) -> str:
        return """DO $$ DECLARE
    r RECORD;
BEGIN
    -- Drop all tables
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
    -- Drop all types
    FOR r IN (SELECT typname FROM pg_type WHERE typnamespace = (SELECT oid FROM pg_namespace WHERE nspname = current_schema())
    AND typname NOT LIKE '\\_%'
    ) LOOP
        EXECUTE 'DROP TYPE IF EXISTS ' || quote_ident(r.typname) || ' CASCADE';
    END LOOP;
END $$;"""


class TestDatabaseSettings(DatabaseSettings):
    user_name: str = Field(default="")
    password: str = Field(default="")
    sql_server: str = Field(default="")
    sql_db: str = Field(default="")
    port: int = Field(default=0)

    @property
    def database_url(self) -> str:
        return "sqlite://"

    @property
    def engine_properties(self) -> dict:
        return dict(connect_args={"check_same_thread": False}, poolclass=StaticPool)

    @property
    def drop_all_tables_query(self) -> str:
        return "SELECT 'DROP TABLE IF EXISTS ' || name || ';' FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%';"
