from venv import logger
from src.features.event.schemas import (
    EventCreate,
    EventFilter,
    EventPaginationFilter,
    EventTranslationIn,
)
from src.features.event.operation import EventOperation
from src.integrations.minio.helpers import generate_random_filename
from src.integrations.minio.repository import MinioStorageProvider


class EventComponent:
    def __init__(
        self,
        event_operation: EventOperation,
    ):
        self.__event_operation = event_operation

    def get_event(self, event_id: int, filter: EventFilter):
        return self.__event_operation.get_event_by_id(event_id, filter)

    def get_all_events(self, mosque_id: int, filter: EventPaginationFilter):
        return self.__event_operation.get_all_events(mosque_id, filter)

    def create_event(
        self,
        event_create: EventCreate,
    ):
        return self.__event_operation.create(event_create)

    def create_event_translation(
        self,
        event_id: int,
        event_translation_in: EventTranslationIn,
        minio_provider: MinioStorageProvider,
    ):
        dir_path = f"/events/event_{event_id}"
        files_uploaded = []

        try:
            for media_file in event_translation_in.media:
                file = media_file.file.read()
                file_name = media_file.filename
                stored_file_name = generate_random_filename(original_filename=file_name)
                minio_provider.upload_bytes(
                    filename=f"{dir_path}/{stored_file_name}", data=file
                )
                files_uploaded.append(f"{dir_path}/{stored_file_name}")
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

        return self.__event_operation.create_event_translation(
            event_id, event_translation_in, dir_path
        )
