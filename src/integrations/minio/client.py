from __future__ import annotations


from minio import Minio
import urllib3

from src.integrations.minio.settings import MinioSettings


class MinioClientFactory:
    """
    Builds a single MinIO client. If `proxy_url` is set, requests are sent through
    an HTTP proxy while preserving the configured endpoint host for URL generation.
    """

    def __init__(self) -> None:
        self._settings = MinioSettings()

    def create(self) -> Minio:
        http_client = (
            urllib3.ProxyManager(proxy_url=self._settings.proxy_url)
            if self._settings.proxy_url
            else None
        )

        return Minio(
            endpoint=self._settings.endpoint,
            access_key=self._settings.access_key,
            secret_key=self._settings.secret_key,
            secure=self._settings.secure,
            http_client=http_client,
        )
