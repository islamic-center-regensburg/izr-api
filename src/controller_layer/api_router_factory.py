from enum import Enum
from typing import Any

from fastapi import APIRouter

from src.controller_layer.models import HttpError

DEFAULT_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {"description": "Bad Request", "model": HttpError},
    401: {"description": "Unauthorized", "model": HttpError},
    403: {"description": "Forbidden", "model": HttpError},
    404: {"description": "Not found", "model": HttpError},
    409: {"description": "Conflict", "model": HttpError},
    422: {"description": "Unprocessable Entity", "model": HttpError},
    500: {"description": "Internal Server Error", "model": HttpError},
}


def create_default_router(
    prefix: str, tags: list[str | Enum] | None = None
) -> APIRouter:
    return APIRouter(prefix=prefix, tags=tags, responses=DEFAULT_RESPONSES)
