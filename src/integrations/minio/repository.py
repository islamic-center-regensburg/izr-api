from __future__ import annotations

import mimetypes
from datetime import timedelta
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error

from src.integrations.minio.enums import DirectoryEnum
from .settings import MinioSettings


class MinioStorageProvider:
    """
    Uses one MinIO client for all S3 operations, including presigned URL generation.
    """

    def __init__(
        self,
        *,
        client: Minio,
        directory: DirectoryEnum | None = None,
    ) -> None:
        self._client = client
        self._settings = MinioSettings()
        self._directory = directory

    @property
    def bucket(self) -> str:
        return self._settings.bucket

    @property
    def directory(self) -> str:
        return self.to_dir_name(self._directory)

    def to_dir_name(self, dir_enum: DirectoryEnum) -> str:
        match dir_enum:
            case DirectoryEnum.PRAYER_TIMES:
                return self._settings.prayer_times_directory
            case DirectoryEnum.DB_BACKUPS:
                return self._settings.db_backups_directory
            case DirectoryEnum.MEDIA:
                return self._settings.media_directory
            case None:
                return ""
            case _:
                raise ValueError(f"Unsupported directory enum: {dir_enum!r}")

    def _prefix(self) -> str:
        return self.directory.strip("/")

    def _object_key(self, name: str) -> str:
        prefix = self._prefix()
        name = name.lstrip("/")
        if prefix and (name == prefix or name.startswith(f"{prefix}/")):
            return name
        return f"{prefix}/{name}" if prefix else name

    def _guess_content_type(self, filename: str) -> str:
        guessed, _ = mimetypes.guess_type(filename)
        return guessed or "application/octet-stream"

    def list_objects(self, prefix: str = "") -> list[str]:
        full_prefix = self._object_key(prefix)
        objects = self._client.list_objects(
            self.bucket, prefix=full_prefix, recursive=True
        )
        return [obj.object_name for obj in objects]

    def ensure_bucket(self) -> None:
        bucket = self.bucket
        if not self._client.bucket_exists(bucket):
            self._client.make_bucket(bucket)

    def ensure_directory_marker(self) -> None:
        """
        Optional: creates a zero-byte object `dir/` so MinIO Console shows the folder even if empty.
        Not required for normal operation.
        """
        import io

        self.ensure_bucket()
        marker_key = self._prefix() + "/"
        try:
            self._client.put_object(self.bucket, marker_key, io.BytesIO(b""), 0)
        except S3Error:
            pass

    def upload_bytes(
        self,
        *,
        filename: str,
        data: bytes,
        content_type: str | None = None,
    ) -> None:
        import io

        self.ensure_bucket()
        resolved_content_type = content_type or self._guess_content_type(filename)
        self._client.put_object(
            bucket_name=self.bucket,
            object_name=self._object_key(filename),
            data=io.BytesIO(data),
            length=len(data),
            content_type=resolved_content_type,
        )

    def upload_fileobj(
        self,
        *,
        filename: str,
        fileobj: BinaryIO,
        length: int,
        content_type: str | None = None,
    ) -> None:
        self.ensure_bucket()
        resolved_content_type = content_type or self._guess_content_type(filename)
        self._client.put_object(
            bucket_name=self.bucket,
            object_name=self._object_key(filename),
            data=fileobj,
            length=length,
            content_type=resolved_content_type,
        )

    def presigned_get_url(
        self,
        *,
        filename: str,
        expires: int = 3600,
        inline: bool = True,
    ) -> str:
        """
        Generate a presigned URL using the configured endpoint.
        """
        response_headers: dict[str, str] = {}

        if inline:
            response_headers["response-content-disposition"] = "inline"

        return self._client.presigned_get_object(
            bucket_name=self.bucket,
            object_name=self._object_key(filename),
            expires=timedelta(seconds=expires),
            response_headers=response_headers or None,
        )

    def delete(self, filename: str) -> None:
        self._client.remove_object(self.bucket, self._object_key(filename))
