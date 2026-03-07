from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )

    endpoint: str = Field(
        default="minio:9000",
        validation_alias=AliasChoices("MINIO_ENDPOINT", "MINIO_PRIVATE_ENDPOINT"),
        description="MinIO endpoint host:port, e.g. 'minio:9000'.",
    )
    secure: bool = Field(
        default=False,
        validation_alias=AliasChoices("MINIO_SECURE", "MINIO_PRIVATE_SECURE"),
        description="Use HTTPS for endpoint.",
    )
    proxy_url: str | None = Field(
        default=None,
        alias="MINIO_PROXY_URL",
        description="Optional HTTP proxy URL used by the MinIO client.",
    )

    # credentials / bucket
    access_key: str = Field(..., alias="MINIO_ROOT_USER")
    secret_key: str = Field(..., alias="MINIO_ROOT_PASSWORD")
    bucket: str = Field(..., alias="MINIO_DEFAULT_BUCKET", description="Default bucket")

    # directories
    prayer_times_directory: str = Field(
        default="prayer-times", alias="PRAYER_TIMES_DIRECTORY"
    )
    db_backups_directory: str = Field(
        default="db-backups", alias="DB_BACKUPS_DIRECTORY"
    )
    media_directory: str = Field(default="media", alias="MEDIA_DIRECTORY")
