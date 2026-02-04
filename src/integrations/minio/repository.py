from __future__ import annotations

from datetime import timedelta
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error

from src.integrations.minio.enums import DirectoryEnum
from .settings import MinioSettings


class MinioStorageProvider:
    def __init__(
        self,
        client: Minio,
        settings: MinioSettings,
        directory: DirectoryEnum,
    ) -> None:
        self._client = client
        self._settings = settings
        self._directory = directory

    @property
    def bucket(self) -> str:
        return self._settings.bucket

    @property
    def directory(self) -> str:
        match self._directory:
            case DirectoryEnum.PRAYER_TIMES:
                return self._settings.prayer_times_directory
            case DirectoryEnum.DB_BACKUPS:
                return self._settings.db_backups_directory
            case DirectoryEnum.MEDIA:
                return self._settings.media_directory
            case _:
                raise ValueError(f"Unsupported directory enum: {self._directory!r}")

    def _prefix(self) -> str:
        # keep it consistent and safe
        return self.directory.strip("/")

    def _object_key(self, name: str) -> str:
        # `name` can be a filename or a relative path like "mosque-1/2026.csv"
        prefix = self._prefix()
        name = name.lstrip("/")
        return f"{prefix}/{name}" if prefix else name

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
            # ignore if it already exists or if server rejects folder markers
            pass

    def upload_bytes(
        self,
        *,
        filename: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> None:
        import io

        self.ensure_bucket()
        self._client.put_object(
            bucket_name=self.bucket,
            object_name=self._object_key(filename),
            data=io.BytesIO(data),
            length=len(data),
            content_type=content_type,
        )

    def upload_fileobj(
        self,
        *,
        filename: str,
        fileobj: BinaryIO,
        length: int,
        content_type: str = "application/octet-stream",
    ) -> None:
        self.ensure_bucket()
        self._client.put_object(
            bucket_name=self.bucket,
            object_name=self._object_key(filename),
            data=fileobj,
            length=length,
            content_type=content_type,
        )

    def presigned_get_url(
        self,
        *,
        filename: str,
        expires: int = 3600,
        content_type: str | None = None,
        inline: bool = True,
    ) -> str:
        response_headers: dict[str, str] = {}

        # Force preview in browser (when the browser supports the type)
        if inline:
            response_headers["response-content-disposition"] = "inline"
            # If you want to preserve the filename in the Save dialog, you can do:
            # response_headers["response-content-disposition"] = f'inline; filename="{filename}"'

        # Set the correct mime type (image/png, video/mp4, etc.)
        if content_type:
            response_headers["response-content-type"] = content_type

        return self._client.presigned_get_object(
            bucket_name=self.bucket,
            object_name=self._object_key(filename),
            expires=timedelta(seconds=expires),
            response_headers=response_headers or None,
        )

    def delete(self, filename: str) -> None:
        self._client.remove_object(self.bucket, self._object_key(filename))
