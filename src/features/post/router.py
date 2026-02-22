from fastapi import APIRouter

from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.post.component import PostComponent
from src.features.post.controller import PostController
from src.features.post.operation import PostOperation, PostTranslationOperation
from src.features.mosque.operation import MosqueOperation


def get_router(db_respository_provider: DatabaseRepositoryProvider) -> APIRouter:
    mosque_operation = MosqueOperation(db_respository_provider)
    operation = PostOperation(db_respository_provider)
    translation_operation = PostTranslationOperation(db_respository_provider)
    component = PostComponent(operation, translation_operation, mosque_operation)
    controller = PostController(component)
    return controller.get_router()
