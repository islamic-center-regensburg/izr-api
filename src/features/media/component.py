from src.features.media.exception import DeleteMediaException, GetMediaException
from src.features.media.schemas import DirectoryQuery, MediaOut
from src.integrations.minio.repository import MinioStorageProvider


class MediaComponent:
    def get_all_media_in_directory(
        self,
        query: DirectoryQuery,
        minio_provider: MinioStorageProvider,
    ) -> list[MediaOut]:
        path = f"{minio_provider.to_dir_name(query.media_category)}/{query.mosque_id}/{query.dir}"

        objects = minio_provider.list_objects(prefix=path)
        media_list = []
        for obj in objects:
            try:
                url = minio_provider.presigned_get_url(filename=obj)
                media_list.append(
                    MediaOut(object="/".join(obj.split("/")[2:]), url=url)
                )
            except Exception as e:
                raise GetMediaException(f"Failed to get media: {str(e)}") from e
        return media_list

    def delete_all_media_in_directory(
        self,
        query: DirectoryQuery,
        minio_provider: MinioStorageProvider,
    ) -> None:
        path = f"{minio_provider.to_dir_name(query.media_category)}/{query.mosque_id}/{query.dir}"
        objects = minio_provider.list_objects(prefix=path)
        for obj in objects:
            try:
                minio_provider.delete(obj)
            except Exception as e:
                raise DeleteMediaException(f"Failed to delete media: {str(e)}") from e
