from typing import Generator

from src.integrations.minio.client import MinioClientFactory
from src.integrations.minio.enums import DirectoryEnum
from src.integrations.minio.repository import MinioStorageProvider


def get_minio_repository() -> Generator[MinioStorageProvider, None, None]:
    client_factory = MinioClientFactory()

    minio_provider = MinioStorageProvider(
        client=client_factory.create(),
        directory=DirectoryEnum.MEDIA,
    )
    yield minio_provider
