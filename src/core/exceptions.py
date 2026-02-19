from __future__ import annotations

from functools import wraps
import inspect
from typing import ParamSpec, TypeVar

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError as CoreValidationError

from src.core.db.database_repository import DoesNotExistInDatabaseException
from src.core.logging.logger import logger
from src.features.post.exception import PostTranslationAlreadyExists
from src.features.media.exception import DeleteMediaException, GetMediaException

P = ParamSpec("P")
R = TypeVar("R")


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())},
    )


async def core_validation_exception_handler(
    request: Request,
    exc: CoreValidationError,
):
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())},
    )


EXCEPTION_MAPPINGS = [
    (DoesNotExistInDatabaseException, 404, "warning", "Database error"),
    (GetMediaException, 400, "warning", "Media error"),
    (DeleteMediaException, 400, "warning", "Media error"),
    (PostTranslationAlreadyExists, 400, "error", "Post translation error"),
]


def guard(fn):
    if inspect.iscoroutinefunction(fn):

        @wraps(fn)
        async def _w(*args, **kwargs):
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                # Check mapped exceptions
                for exc_class, status_code, log_level, log_msg in EXCEPTION_MAPPINGS:
                    if isinstance(e, exc_class):
                        getattr(logger, log_level)(f"{log_msg}: {e}")
                        raise HTTPException(
                            status_code=status_code, detail=str(log_msg)
                        )

                # Unhandled exception
                logger.error(f"Unhandled exception: {e}")
                raise HTTPException(status_code=500, detail="Internal Server Error")

        return _w

    @wraps(fn)
    def _w(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            # Check mapped exceptions
            for exc_class, status_code, log_level, log_msg in EXCEPTION_MAPPINGS:
                if isinstance(e, exc_class):
                    getattr(logger, log_level)(f"{log_msg}: {e}")
                    raise HTTPException(status_code=status_code, detail=str(e))

            # Unhandled exception
            logger.error(f"Unhandled exception: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return _w
