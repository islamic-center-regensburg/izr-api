from typing import Generator

from src.integrations.minio.client import MinioClientFactory
from src.integrations.minio.enums import DirectoryEnum
from src.integrations.minio.repository import MinioStorageProvider
from src.integrations.minio.settings import get_minio_settings


def get_minio_repository() -> Generator[MinioStorageProvider, None, None]:
    settings = get_minio_settings()
    clients = MinioClientFactory(settings).create()

    repo = MinioStorageProvider(
        private_client=clients.private,
        public_client=clients.public,
        settings=settings,
        directory=DirectoryEnum.MEDIA,
    )
    yield repo
