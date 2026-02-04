from fastapi import APIRouter

from src.features.prayer_iqama.component import PrayerIqamaComponent
from src.features.prayer_iqama.controller import PrayerIqamaController
from src.features.prayer_iqama.operation import (
    PrayerIqamaOperation,
)


def get_router(database_repository_provider) -> APIRouter:
    prayer_iqama_operation = PrayerIqamaOperation(database_repository_provider)

    component = PrayerIqamaComponent(
        prayer_iqama_operation=prayer_iqama_operation,
    )

    controller = PrayerIqamaController(component)
    return controller.get_router()
