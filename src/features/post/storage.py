from typing import Generator

from src.integrations.minio.client import MinioClientFactory
from src.integrations.minio.enums import DirectoryEnum
from src.integrations.minio.repository import MinioStorageProvider
from src.integrations.minio.settings import get_minio_settings


def get_minio_repository() -> Generator[MinioStorageProvider, None, None]:
    settings = get_minio_settings()
    client = MinioClientFactory(settings).create()
    repo = MinioStorageProvider(client, settings, directory=DirectoryEnum.MEDIA)
    try:
        yield repo
    finally:
        pass
