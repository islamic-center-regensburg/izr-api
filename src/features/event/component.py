from uuid import UUID
from venv import logger
from src.features.event.exception import EventTranslationAlreadyExists
from src.features.event.schemas import (
    EventCreate,
    EventFilter,
    EventPaginationFilter,
    EventTranslationIn,
)
from src.features.event.operation import EventOperation
from src.features.mosque.operation import MosqueOperation
from src.integrations.minio.helpers import generate_random_filename
from src.integrations.minio.repository import MinioStorageProvider


class EventComponent:
    def __init__(
        self,
        event_operation: EventOperation,
        mosque_operation: MosqueOperation,
    ):
        self.__event_operation = event_operation
        self.mosque_operation = mosque_operation

    def get_event(self, event_id: UUID, filter: EventFilter):
        return self.__event_operation.get_event_by_id(event_id, filter)

    def get_all_events(self, mosque_id: UUID, filter: EventPaginationFilter):
        return self.__event_operation.get_all_events(mosque_id, filter)

    def create_event(
        self,
        event_create: EventCreate,
    ):
        return self.__event_operation.create(event_create)

    def create_event_translation(
        self,
        mosque_id: UUID,
        event_id: UUID,
        event_translation_in: EventTranslationIn,
        description: str | None,
        minio_provider: MinioStorageProvider,
    ):
        event = self.__event_operation.get_event_by_id(
            event_id, EventFilter(language=event_translation_in.language)
        )

        if len(event.translations):
            msg = f"Translation for event {event_id} in language '{event_translation_in.language}' already exists."
            raise EventTranslationAlreadyExists(msg)

        mosque = self.mosque_operation.get_mosque_by_id(mosque_id)

        db_dir_path = f"events/event_{event_id}/{event_translation_in.language}"
        minio_dir_path = (
            f"{mosque.id}/events/event_{event_id}/{event_translation_in.language}"
        )
        files_uploaded = []

        if event_translation_in.media:
            try:
                for media_file in event_translation_in.media:
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

        return self.__event_operation.create_event_translation(
            event_id, event_translation_in, description, db_dir_path
        )
