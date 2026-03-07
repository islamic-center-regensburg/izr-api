from uuid import UUID
from venv import logger
from src.features.post.adapter import PostAdapter
from src.features.post.enums import AllowedMediaType
from src.features.post.exception import (
    DeleteMediaException,
    GetMediaException,
    PostTranslationAlreadyExists,
)
from src.features.post.schemas import (
    MediaOut,
    PostCreate,
    PostFilter,
    PostListOut,
    PostOut,
    PostPaginationFilter,
    PostTranslationMediaIn,
    PostTranslationMetaIn,
    PostTranslationRead,
    PostTranslationUpdate,
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

    def update_post_translation(
        self,
        post_id: UUID,
        translation_id: UUID,
        post_translation_update: PostTranslationUpdate,
        description: str | None,
    ) -> PostTranslationRead:
        return self.__post_translation_operation.update_post_translation(
            post_id, translation_id, post_translation_update, description
        )

    def delete_post_translation(
        self,
        post_id: UUID,
        translation_id: UUID,
        minio_provider: MinioStorageProvider,
    ) -> bool:
        post = self.__post_operation.get_post_by_id(post_id, PostFilter())
        post_translation = self.__post_translation_operation.get_post_translation_by_id(
            translation_id
        )

        if post_translation.media:
            self.__delete_all_media_in_directory(
                mosque_id=post.mosque_id,
                dir=post_translation.media,
                minio_provider=minio_provider,
            )

        self.__post_translation_operation.delete_post_translation(
            post_id,
            translation_id,
        )
        return True

    def delete_post_media(
        self,
        translation_id: UUID,
        file_path: str | None,
        minio_provider: MinioStorageProvider,
    ) -> PostTranslationRead:
        post_translation = self.__post_translation_operation.get_post_translation_by_id(
            translation_id
        )

        if post_translation.media:
            post = self.__post_operation.get_post_by_id(
                post_translation.post_id, PostFilter()
            )
        dir_to_delete = (
            file_path if file_path else f"{post.mosque_id}/{post_translation.media}"
        )
        self.__delete_all_media_in_directory(
            dir=dir_to_delete,
            minio_provider=minio_provider,
        )

        try:
            remaining_files = self.__get_all_media_in_directory(
                dir=f"{post.mosque_id}/{post_translation.media}",
                minio_provider=minio_provider,
            )

            if not file_path and len(remaining_files) == 0:
                return self.__post_translation_operation.clear_post_translation_media(
                    translation_id,
                )
            else:
                raise Exception("Media files still exist for the post translation")
        except Exception:
            return self.__post_translation_operation.get_post_translation_by_id(
                translation_id,
            )

    def delete_post(
        self,
        post_id: UUID,
        minio_provider: MinioStorageProvider,
    ) -> bool:
        post = self.__post_operation.get_post_by_id(post_id, PostFilter())
        post_translations = self.__post_translation_operation.get_post_translations(
            post_id,
            None,
        )

        dir = f"{post.mosque_id}/posts/post_{post_id}"

        for post_translation in post_translations:
            if post_translation.media:
                self.__delete_all_media_in_directory(
                    dir=dir,
                    minio_provider=minio_provider,
                )
            self.__post_translation_operation.delete_post_translation(
                post_id,
                post_translation.id,
            )

        self.__post_operation.delete_post(post_id)
        return True

    def create_post_translation(
        self,
        post_id: UUID,
        post_translation_in: PostTranslationMetaIn,
        post_translation_description: str | None = None,
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

        return self.__post_translation_operation.create_post_translation(
            post_id,
            post_translation_in,
            description=post_translation_description,
        )

    async def upload_post_media(
        self,
        translation_id: UUID,
        media_in: PostTranslationMediaIn,
        minio_provider: MinioStorageProvider,
    ) -> PostTranslationRead:
        post_translation = self.__post_translation_operation.get_post_translation_by_id(
            translation_id
        )
        post = self.__post_operation.get_post_by_id(
            post_translation.post_id,
            PostFilter(),
        )

        db_dir_path = (
            f"posts/post_{post_translation.post_id}/{post_translation.language}"
        )
        minio_dir_path = f"{post.mosque_id}/{db_dir_path}"

        await validate_upload_type(
            files=media_in.media,
            allowed=AllowedMediaType,
        )

        files_uploaded = []
        try:
            for media_file in media_in.media:
                file = media_file.file.read()
                stored_file_name = generate_random_filename(
                    original_filename=media_file.filename
                )
                object_key = f"{minio_dir_path}/{stored_file_name}"
                minio_provider.upload_bytes(filename=object_key, data=file)
                files_uploaded.append(object_key)
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

        return self.__post_translation_operation.set_post_translation_media(
            translation_id,
            db_dir_path,
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
                    MediaOut(object="/".join(obj.split("/")[1:]), url=url)
                )
            except Exception as e:
                raise GetMediaException(f"Failed to get media: {str(e)}") from e

        return media_list

    def __delete_all_media_in_directory(
        self,
        dir: str,
        minio_provider: MinioStorageProvider,
    ) -> None:
        objects = minio_provider.list_objects(prefix=dir)
        for obj in objects:
            try:
                minio_provider.delete(obj)
            except Exception as e:
                raise DeleteMediaException(f"Failed to delete media: {str(e)}") from e
