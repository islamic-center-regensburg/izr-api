from __future__ import annotations

from dataclasses import dataclass

from minio import Minio


@dataclass(frozen=True, slots=True)
class MinioClientConfig:
    endpoint: str
    access_key: str
    secret_key: str
    secure: bool


class MinioClientFactory:
    """
    Builds two MinIO clients:
      - private: for internal Docker network traffic (e.g. endpoint "minio:9000", secure=False)
      - public:  for generating presigned URLs with the real domain (e.g. "s3.iz-regensburg.de", secure=True)
    """

    def __init__(
        self, *, private: MinioClientConfig, public: MinioClientConfig
    ) -> None:
        self._private = private
        self._public = public

    def create_private(self) -> Minio:
        return Minio(
            endpoint=self._private.endpoint,
            access_key=self._private.access_key,
            secret_key=self._private.secret_key,
            secure=self._private.secure,
        )

    def create_public(self) -> Minio:
        return Minio(
            endpoint=self._public.endpoint,
            access_key=self._public.access_key,
            secret_key=self._public.secret_key,
            secure=self._public.secure,
        )
