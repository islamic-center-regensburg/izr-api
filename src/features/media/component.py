from src.core.db.pagination import PageParams, PaginatedResponse
from src.features.media.adapter import MediaAdapter
from src.features.media.enums import AllowedMeidaType
from src.features.media.schemas import MediaCreate, MediaIn, MediaFilter, MediaOut
from src.features.media.operation import MediaOperation
from src.features.mosque.operation import MosqueOperation
from src.integrations.minio.helpers import (
    build_media_object_name,
    generate_random_filename,
)
from src.integrations.minio.repository import MinioStorageProvider
from src.integrations.minio.validator import validate_upload_type


class MediaComponent:
    def __init__(
        self,
        media_operation: MediaOperation,
        mosque_operation: MosqueOperation,
    ):
        self.__media_operation = media_operation
        self.__mosque_operation = mosque_operation

    def get_all_media(
        self, filter: MediaFilter, minio_provider: MinioStorageProvider
    ) -> PaginatedResponse[MediaOut]:
        return MediaAdapter.to_paginated_media_out(
            self.__media_operation.get_all_media(filter), minio_provider
        )

    def get_all_media_for_mosque(
        self,
        mosque_id: int,
        page_params: PageParams,
        minio_provider: MinioStorageProvider,
    ) -> PaginatedResponse[MediaOut]:
        return MediaAdapter.to_paginated_media_out(
            self.__media_operation.get_all_media_for_mosque(mosque_id, page_params),
            minio_provider,
        )

    def get_media_by_id(
        self, media_id: int, minio_provider: MinioStorageProvider
    ) -> MediaOut:
        return MediaAdapter.to_media_out(
            self.__media_operation.get_media_by_id(media_id), minio_provider
        )

    async def create_media(
        self, media_in: MediaIn, minio_provider: MinioStorageProvider
    ) -> MediaOut:
        mosque = self.__mosque_operation.get_mosque_by_id(media_in.mosque_id)
        file = media_in.file
        await validate_upload_type(file, set(AllowedMeidaType))
        store_file_name = generate_random_filename(original_filename=file.filename)

        object_key = build_media_object_name(
            media_type=str(media_in.type),
            original_filename=store_file_name,
            mosque_name=mosque.name,
            mosque_id=mosque.id,
        )

        minio_provider.upload_bytes(
            filename=object_key,
            data=file.file.read(),
        )

        return MediaAdapter.to_media_out(
            self.__media_operation.create(
                MediaCreate(
                    mosque_id=media_in.mosque_id,
                    object_key=object_key,
                    type=media_in.type,
                )
            ),
            minio_provider,
        )

    def delete_media(self, media_id: int, minio_provider: MinioStorageProvider) -> str:
        object_key = self.__media_operation.delete(media_id)
        minio_provider.delete(object_key)
        return "Success"
