from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )

    endpoint: str = Field(
        ...,
        alias="MINIO_ENDPOINT",
        description="Host:port, e.g. 'minio:9000' or 'localhost:9000'",
    )
    access_key: str = Field(..., alias="MINIO_ROOT_USER")
    secret_key: str = Field(..., alias="MINIO_ROOT_PASSWORD")

    secure: bool = Field(default=False, description="Use HTTPS if true")
    bucket: str = Field(
        ..., alias="MINIO_DEFAULT_BUCKET", description="Default bucket name"
    )

    prayer_times_directory: str = Field(
        default="prayer-times", alias="PRAYER_TIMES_DIRECTORY"
    )
    db_backups_directory: str = Field(
        default="db-backups", alias="DB_BACKUPS_DIRECTORY"
    )

    media_directory: str = Field(default="media", alias="MEDIA_DIRECTORY")


# Convenience singleton-ish getter (optional)
_settings: MinioSettings | None = None


def get_minio_settings() -> MinioSettings:
    global _settings
    if _settings is None:
        _settings = MinioSettings()
    return _settings
