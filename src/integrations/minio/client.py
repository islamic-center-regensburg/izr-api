from minio import Minio

from src.integrations.minio.settings import MinioSettings


class MinioClientFactory:
    def __init__(self, settings: MinioSettings) -> None:
        self._settings = settings

    def create(self) -> Minio:
        return Minio(
            endpoint=self._settings.endpoint,
            access_key=self._settings.access_key,
            secret_key=self._settings.secret_key,
            secure=self._settings.secure,
        )
