from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.prayer_times_upload.schemas import (
    PrayerTimeUploadCreate,
    PrayerTimeUploadOut,
    PrayerTimeUploadTable,
)


class PrayerTimesUploadOperation:
    def __init__(
        self,
        db_repository_provider: DatabaseRepositoryProvider,
    ):
        self.__db_repository = db_repository_provider

    def add_prayer_times_upload(
        self, upload: PrayerTimeUploadCreate
    ) -> PrayerTimeUploadOut:
        with self.__db_repository.get_database_repository() as db:
            upload = db.create(
                PrayerTimeUploadTable(
                    year=upload.year,
                    mosque_id=upload.mosque_id,
                    stored_filename=upload.stored_filename,
                    file_type=upload.file_type,
                )
            )
        return upload
