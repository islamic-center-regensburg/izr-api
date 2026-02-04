from fastapi import APIRouter

from src.features.mosque.operation import MosqueOperation
from src.features.prayer_config.component import PrayerConfigComponent
from src.features.prayer_config.controller import PrayerConfigController
from src.features.prayer_config.operation import PrayerConfigOperation


def get_router(
    db_repository_provider,
) -> APIRouter:
    mosque_operation = MosqueOperation(db_repository_provider)
    operation = PrayerConfigOperation(db_repository_provider)
    component = PrayerConfigComponent(
        prayer_config_operation=operation,
        mosque_operation=mosque_operation,
    )
    controller = PrayerConfigController(component)

    return controller.get_router()
