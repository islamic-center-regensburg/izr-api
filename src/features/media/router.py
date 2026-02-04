from fastapi import APIRouter

from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.media.component import MediaComponent
from src.features.media.controller import MediaController
from src.features.media.operation import MediaOperation
from src.features.mosque.operation import MosqueOperation


def get_router(
    db_repository_provider: DatabaseRepositoryProvider,
) -> APIRouter:
    mosque_operation = MosqueOperation(db_repository_provider)
    operation = MediaOperation(db_repository_provider)
    component = MediaComponent(operation, mosque_operation)
    controller = MediaController(component)
    return controller.get_router()
