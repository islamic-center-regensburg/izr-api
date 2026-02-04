from fastapi import APIRouter

from src.features.mosque.component import MosqueComponent
from src.features.mosque.controller import MosqueController
from src.features.mosque.operation import MosqueOperation
from src.features.prayer_config.operation import PrayerConfigOperation


def get_router(
    db_repository_provider,
) -> APIRouter:
    operation = MosqueOperation(db_repository_provider)
    prayer_config_operation = PrayerConfigOperation(db_repository_provider)
    component = MosqueComponent(
        mosque_operation=operation,
        prayer_config_operation=prayer_config_operation,
    )
    controller = MosqueController(component)

    return controller.get_router()
