from typing import Generator
from src.integrations.minio.client import MinioClientConfig, MinioClientFactory
from src.integrations.minio.enums import DirectoryEnum
from src.integrations.minio.repository import MinioStorageProvider
from src.integrations.minio.settings import get_minio_settings
from src.integrations.prayer_times_parser.repository import PrayerTimesParserProvider


def get_minio_repository() -> Generator[MinioStorageProvider, None, None]:
    settings = get_minio_settings()
    client_factory = MinioClientFactory(
        private=MinioClientConfig(
            endpoint=settings.private_endpoint,
            access_key=settings.access_key,
            secret_key=settings.secret_key,
            secure=settings.private_secure,
        ),
        public=MinioClientConfig(
            endpoint=settings.public_endpoint,
            access_key=settings.access_key,
            secret_key=settings.secret_key,
            secure=settings.public_secure,
        ),
    )

    repo = MinioStorageProvider(
        private_client=client_factory.create_private(),
        public_client=client_factory.create_public(),
        settings=settings,
        directory=DirectoryEnum.PRAYER_TIMES,
    )
    yield repo


def get_prayer_times_parser_repository() -> (
    Generator["PrayerTimesParserProvider", None, None]
):
    repo = PrayerTimesParserProvider()
    try:
        yield repo
    finally:
        pass
