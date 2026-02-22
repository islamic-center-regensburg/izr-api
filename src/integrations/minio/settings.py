from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )

    # PRIVATE / internal (Docker network) endpoint: used for upload/list/delete/etc.
    private_endpoint: str = Field(
        default="minio:9000",
        alias="MINIO_PRIVATE_ENDPOINT",
        description="Host:port for internal traffic, e.g. 'minio:9000'",
    )
    private_secure: bool = Field(
        default=False,
        alias="MINIO_PRIVATE_SECURE",
        description="Use HTTPS for private endpoint (usually false in compose).",
    )

    # PUBLIC endpoint: used ONLY for generating presigned URLs for browsers/clients
    public_endpoint: str = Field(
        default="s3.iz-regensburg.de",
        alias="MINIO_PUBLIC_ENDPOINT",
        description="Public S3 domain behind Caddy, e.g. 's3.iz-regensburg.de'",
    )
    public_secure: bool = Field(
        default=True,
        alias="MINIO_PUBLIC_SECURE",
        description="Use HTTPS for public endpoint (usually true).",
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

    # Backward-compatible aliases (optional):
    # If other code still reads settings.endpoint/settings.secure,
    # make them resolve to the private endpoint.
    @property
    def endpoint(self) -> str:  # keeps old code working if needed
        return self.private_endpoint

    @property
    def secure(self) -> bool:  # keeps old code working if needed
        return self.private_secure


_settings: MinioSettings | None = None


def get_minio_settings() -> MinioSettings:
    global _settings
    if _settings is None:
        _settings = MinioSettings()
    return _settings
