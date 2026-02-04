from typing import Generator
from src.integrations.minio.client import MinioClientFactory
from src.integrations.minio.enums import DirectoryEnum
from src.integrations.minio.repository import MinioStorageProvider
from src.integrations.minio.settings import get_minio_settings
from src.integrations.prayer_times_parser.repository import PrayerTimesParserProvider


def get_minio_repository() -> Generator[MinioStorageProvider, None, None]:
    settings = get_minio_settings()
    client = MinioClientFactory(settings).create()
    repo = MinioStorageProvider(client, settings, directory=DirectoryEnum.PRAYER_TIMES)
    try:
        yield repo
    finally:
        pass


def get_prayer_times_parser_repository() -> (
    Generator["PrayerTimesParserProvider", None, None]
):
    repo = PrayerTimesParserProvider()
    try:
        yield repo
    finally:
        pass
