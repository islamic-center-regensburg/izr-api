from fastapi import APIRouter

from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.event.component import EventComponent
from src.features.event.controller import EventController
from src.features.event.operation import EventOperation


def get_router(db_respository_provider: DatabaseRepositoryProvider) -> APIRouter:
    operation = EventOperation(db_respository_provider)
    component = EventComponent(operation)
    controller = EventController(component)
    return controller.get_router()
