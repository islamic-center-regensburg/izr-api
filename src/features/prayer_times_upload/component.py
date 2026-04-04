from src.features.mosque.operation import MosqueOperation
from src.features.prayer_times.models.schemas import StoredPrayerTimesCreate
from src.features.prayer_times.operation import PrayerTimesOperation
from src.features.prayer_times_upload.operation import PrayerTimesUploadOperation
from src.features.prayer_times_upload.schemas import (
    PrayerTimeUploadCreate,
    PrayerTimeUploadIn,
    PrayerTimeUploadOut,
)
from src.integrations.minio.repository import MinioStorageProvider
from src.integrations.prayer_times_parser.repository import PrayerTimesParserProvider


class PrayerTimesUploadComponent:
    def __init__(
        self,
        prayer_times_upload_operation: PrayerTimesUploadOperation,
        prayer_times_operation: PrayerTimesOperation,
        mosque_operation: MosqueOperation,
    ):
        self.__prayer_times_upload_operation = prayer_times_upload_operation
        self.__prayer_times_operation = prayer_times_operation
        self.__mosque_operation = mosque_operation

    def upload_prayer_times(
        self,
        prayer_time_upload_in: PrayerTimeUploadIn,
        minio_provider: MinioStorageProvider,
        prayer_times_parser_provider: PrayerTimesParserProvider,
    ) -> PrayerTimeUploadOut:
        parser = prayer_times_parser_provider.get_parser(
            prayer_time_upload_in.file_type
        )

        mosque = self.__mosque_operation.get_mosque_by_id(
            prayer_time_upload_in.mosque_id
        )
        mosque_name_cleaned = mosque.name.lower().replace(" ", "_")
        stored_file_name = f"{mosque.id}/{mosque_name_cleaned}_prayer_times_{prayer_time_upload_in.year}.{prayer_time_upload_in.file_type}"

        data = prayer_time_upload_in.file.file.read()
        minio_provider.upload_bytes(
            filename=stored_file_name,
            data=data,
        )

        upload = self.__prayer_times_upload_operation.add_prayer_times_upload(
            PrayerTimeUploadCreate(
                mosque_id=prayer_time_upload_in.mosque_id,
                year=prayer_time_upload_in.year,
                stored_filename=stored_file_name,
                file_type=prayer_time_upload_in.file_type,
            )
        )

        rows: list[StoredPrayerTimesCreate] = parser.parse_bytes(data)
        self.__prayer_times_operation.save_prayer_times_rows(
            mosque_id=prayer_time_upload_in.mosque_id, upload_id=upload.id, rows=rows
        )

        return upload
