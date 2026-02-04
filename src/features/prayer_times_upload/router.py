from fastapi import APIRouter

from src.features.mosque.operation import MosqueOperation
from src.features.prayer_times.operation import PrayerTimesOperation
from src.features.prayer_times_upload.component import PrayerTimesUploadComponent
from src.features.prayer_times_upload.controller import PrayerTimesUploadController
from src.features.prayer_times_upload.operation import PrayerTimesUploadOperation


def get_router(
    db_repository_provider,
) -> APIRouter:
    mosque_operation = MosqueOperation(db_repository_provider)
    prayer_times_operation = PrayerTimesOperation(db_repository_provider)

    operation = PrayerTimesUploadOperation(
        db_repository_provider=db_repository_provider,
    )
    component = PrayerTimesUploadComponent(
        prayer_times_upload_operation=operation,
        prayer_times_operation=prayer_times_operation,
        mosque_operation=mosque_operation,
    )

    controller = PrayerTimesUploadController(component)

    return controller.get_router()
