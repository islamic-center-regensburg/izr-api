from uuid import UUID
from venv import logger
from src.features.media.exception import DeleteMediaException, GetMediaException
from src.features.media.schemas import MediaOut
from src.features.post.adapter import PostAdapter
from src.features.post.enums import AllowedMediaType
from src.features.post.exception import PostTranslationAlreadyExists
from src.features.post.schemas import (
    PostCreate,
    PostFilter,
    PostListOut,
    PostOut,
    PostPaginationFilter,
    PostTranslationIn,
)
from src.features.post.operation import PostOperation, PostTranslationOperation
from src.features.mosque.operation import MosqueOperation
from src.integrations.minio.helpers import generate_random_filename
from src.integrations.minio.repository import MinioStorageProvider
from src.integrations.minio.validator import validate_upload_type


class PostComponent:
    def __init__(
        self,
        post_operation: PostOperation,
        post_translation_operation: PostTranslationOperation,
        mosque_operation: MosqueOperation,
    ):
        self.__post_operation = post_operation
        self.__post_translation_operation = post_translation_operation
        self.mosque_operation = mosque_operation

    def get_post(
        self, post_id: UUID, filter: PostFilter, minio_provider: MinioStorageProvider
    ) -> PostOut:
        post = self.__post_operation.get_post_by_id(post_id, filter)
        post.translations = self.__post_translation_operation.get_post_translations(
            post.id,
            filter.language,
        )
        return PostAdapter.to_post_out(
            post=post,
            get_media_in_directory=lambda mosque_id, dir: (
                self.__get_all_media_in_directory(
                    mosque_id=mosque_id,
                    dir=dir,
                    minio_provider=minio_provider,
                )
            ),
        )

    def get_all_posts(
        self,
        mosque_id: UUID,
        filter: PostPaginationFilter,
        minio_provider: MinioStorageProvider,
    ) -> PostListOut:
        posts = self.__post_operation.get_all_posts(mosque_id, filter)
        for post in posts.data:
            post.translations = self.__post_translation_operation.get_post_translations(
                post.id,
                filter.language,
            )
        return PostAdapter.to_post_list_out(
            posts=posts,
            get_media_in_directory=lambda mosque_id, dir: (
                self.__get_all_media_in_directory(
                    mosque_id=mosque_id,
                    dir=dir,
                    minio_provider=minio_provider,
                )
            ),
        )

    def create_post(
        self,
        post_create: PostCreate,
    ):
        return self.__post_operation.create(post_create)

    async def create_post_translation(
        self,
        mosque_id: UUID,
        post_id: UUID,
        post_translation_in: PostTranslationIn,
        description: str | None,
        minio_provider: MinioStorageProvider,
    ):
        post = self.__post_operation.get_post_by_id(
            post_id, PostFilter(language=post_translation_in.language)
        )

        post.translations = self.__post_translation_operation.get_post_translations(
            post.id,
            post_translation_in.language,
        )

        if len(post.translations):
            msg = f"Translation for post {post_id} in language '{post_translation_in.language}' already exists."
            raise PostTranslationAlreadyExists(msg)

        mosque = self.mosque_operation.get_mosque_by_id(mosque_id)

        db_dir_path = f"posts/post_{post_id}/{post_translation_in.language}"
        minio_dir_path = (
            f"{mosque.id}/posts/post_{post_id}/{post_translation_in.language}"
        )
        files_uploaded = []

        if post_translation_in.media:
            await validate_upload_type(
                files=post_translation_in.media,
                allowed=AllowedMediaType,
            )
            try:
                for media_file in post_translation_in.media:
                    file = media_file.file.read()
                    file_name = media_file.filename
                    stored_file_name = generate_random_filename(
                        original_filename=file_name
                    )
                    minio_provider.upload_bytes(
                        filename=f"{minio_dir_path}/{stored_file_name}", data=file
                    )
                    files_uploaded.append(f"{minio_dir_path}/{stored_file_name}")
            except Exception as e:
                logger.error(f"Error uploading files to Minio: {e}")
                for file_path in files_uploaded:
                    try:
                        minio_provider.delete(file_path)
                    except Exception as delete_error:
                        logger.error(
                            f"Error deleting file {file_path} from Minio: {delete_error}"
                        )
                raise e

        return self.__post_translation_operation.create_post_translation(
            post_id, post_translation_in, description, db_dir_path
        )

    def __get_all_media_in_directory(
        self,
        mosque_id: UUID,
        dir: str,
        minio_provider: MinioStorageProvider,
    ) -> list[MediaOut]:
        path = f"{mosque_id}/{dir}"

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

    def __delete_all_media_in_directory(
        self,
        mosque_id: UUID,
        dir: str,
        minio_provider: MinioStorageProvider,
    ) -> None:
        path = f"{mosque_id}/{dir}"
        objects = minio_provider.list_objects(prefix=path)
        for obj in objects:
            try:
                minio_provider.delete(obj)
            except Exception as e:
                raise DeleteMediaException(f"Failed to delete media: {str(e)}") from e
