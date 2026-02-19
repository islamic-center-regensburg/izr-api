from uuid import UUID
from venv import logger
from src.features.post.exception import PostTranslationAlreadyExists
from src.features.post.schemas import (
    PostCreate,
    PostFilter,
    PostPaginationFilter,
    PostTranslationIn,
)
from src.features.post.operation import PostOperation
from src.features.mosque.operation import MosqueOperation
from src.integrations.minio.helpers import generate_random_filename
from src.integrations.minio.repository import MinioStorageProvider


class PostComponent:
    def __init__(
        self,
        post_operation: PostOperation,
        mosque_operation: MosqueOperation,
    ):
        self.__post_operation = post_operation
        self.mosque_operation = mosque_operation

    def get_post(self, post_id: UUID, filter: PostFilter):
        return self.__post_operation.get_post_by_id(post_id, filter)

    def get_all_posts(self, mosque_id: UUID, filter: PostPaginationFilter):
        return self.__post_operation.get_all_posts(mosque_id, filter)

    def create_post(
        self,
        post_create: PostCreate,
    ):
        return self.__post_operation.create(post_create)

    def create_post_translation(
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

        return self.__post_operation.create_post_translation(
            post_id, post_translation_in, description, db_dir_path
        )
