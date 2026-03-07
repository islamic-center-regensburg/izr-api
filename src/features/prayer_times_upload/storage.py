from typing import Generator
from src.integrations.minio.client import MinioClientFactory
from src.integrations.minio.enums import DirectoryEnum
from src.integrations.minio.repository import MinioStorageProvider
from src.integrations.prayer_times_parser.repository import PrayerTimesParserProvider


def get_minio_repository() -> Generator[MinioStorageProvider, None, None]:
    client_factory = MinioClientFactory()

    minio_provider = MinioStorageProvider(
        client=client_factory.create(),
        directory=DirectoryEnum.PRAYER_TIMES,
    )
    yield minio_provider


def get_prayer_times_parser_repository() -> (
    Generator["PrayerTimesParserProvider", None, None]
):
    repo = PrayerTimesParserProvider()
    try:
        yield repo
    finally:
        pass
