from src.core.db.pagination import PaginatedResponse
from src.features.media.enums import MediaFileType
from src.features.media.schemas import MediaOut, MediaTable
from src.integrations.minio.repository import MinioStorageProvider


class MediaAdapter:
    @staticmethod
    def to_paginated_media_out(
        pagination: PaginatedResponse[MediaTable],
        minio_provider: MinioStorageProvider,
    ) -> PaginatedResponse[MediaOut]:
        items = pagination.data
        media_out_list = []
        for media in items:
            content_type = "application/octet-stream"
            if media.type == MediaFileType.IMAGE:
                content_type = "image/png"
            elif media.type == MediaFileType.VIDEO:
                content_type = "video/mp4"

            media_out = MediaOut(
                id=media.id,
                mosque_id=media.mosque_id,
                object_key=media.object_key,
                url=minio_provider.presigned_get_url(
                    filename=media.object_key,
                    content_type=content_type,
                ),
                type=media.type,
            )
            media_out_list.append(media_out)
        pagination.data = media_out_list
        return pagination

    @staticmethod
    def to_media_out(
        media_table: MediaTable,
        minio_provider: MinioStorageProvider,
    ) -> MediaOut:
        content_type = "application/octet-stream"
        if media_table.type == MediaFileType.IMAGE:
            content_type = "image/png"
        elif media_table.type == MediaFileType.VIDEO:
            content_type = "video/mp4"
        return MediaOut(
            id=media_table.id,
            mosque_id=media_table.mosque_id,
            object_key=media_table.object_key,
            url=minio_provider.presigned_get_url(
                filename=media_table.object_key,
                content_type=content_type,
            ),
            type=media_table.type,
        )
