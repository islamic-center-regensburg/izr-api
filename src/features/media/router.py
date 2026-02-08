from fastapi import APIRouter

from src.features.media.component import MediaComponent
from src.features.media.controller import MediaController


def get_router() -> APIRouter:
    component = MediaComponent()
    controller = MediaController(component)
    return controller.get_router()
