from __future__ import annotations

from datetime import timedelta
import traceback
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error

from .settings import MinioSettings


class MinioStorageProvider:
    def __init__(self, client: Minio, settings: MinioSettings) -> None:
        self._client = client
        self._settings = settings

    @property
    def bucket(self) -> str:
        return self._settings.bucket

    def ensure_bucket(self) -> None:
        bucket = self.bucket
        try:
            if not self._client.bucket_exists(bucket):
                self._client.make_bucket(bucket)  # location optional
        except S3Error as e:
            print("S3Error code:", e.code)
            print("S3Error message:", e.message)
            print("S3Error bucket:", getattr(e, "bucket_name", None))
            raise
        except Exception:
            traceback.print_exc()
            raise

    def upload_bytes(
        self,
        *,
        object_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> None:
        # MinIO needs a file-like stream + length
        import io

        self.ensure_bucket()
        stream = io.BytesIO(data)
        self._client.put_object(
            bucket_name=self.bucket,
            object_name=object_name,
            data=stream,
            length=len(data),
            content_type=content_type,
        )

    def upload_fileobj(
        self,
        *,
        object_name: str,
        fileobj: BinaryIO,
        length: int,
        content_type: str = "application/octet-stream",
    ) -> None:
        self.ensure_bucket()
        self._client.put_object(
            bucket_name=self.bucket,
            object_name=object_name,
            data=fileobj,
            length=length,
            content_type=content_type,
        )

    def presigned_get_url(self, *, object_name: str, expires: int = 3600) -> str:
        return self._client.presigned_get_object(
            bucket_name=self.bucket,
            object_name=object_name,
            expires=timedelta(seconds=expires),
        )

    def delete(self, *, object_name: str) -> None:
        self._client.remove_object(self.bucket, object_name)
