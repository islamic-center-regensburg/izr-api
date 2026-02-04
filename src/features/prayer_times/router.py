from fastapi import APIRouter

from src.features.mosque.operation import MosqueOperation
from src.features.prayer_config.operation import PrayerConfigOperation
from src.features.prayer_times.component import PrayerTimesComponent
from src.features.prayer_times.controller import PrayerTimesController
from src.features.prayer_times.operation import PrayerTimesOperation


def get_router(
    db_repository_provider,
) -> APIRouter:
    mosque_operation = MosqueOperation(db_repository_provider)
    prayer_config_operation = PrayerConfigOperation(db_repository_provider)
    operation = PrayerTimesOperation(db_repository_provider)

    component = PrayerTimesComponent(
        prayer_times_operation=operation,
        mosque_operation=mosque_operation,
        prayer_config_operation=prayer_config_operation,
    )

    controller = PrayerTimesController(component)

    return controller.get_router()
