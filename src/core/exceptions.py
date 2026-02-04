from __future__ import annotations

from functools import wraps
import inspect
from typing import ParamSpec, TypeVar

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError as CoreValidationError

from src.core.logging.logger import logger

P = ParamSpec("P")
R = TypeVar("R")


class DoesNotExistInDatabaseException(Exception):
    pass


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


def guard(fn):
    if inspect.iscoroutinefunction(fn):

        @wraps(fn)
        async def _w(*args, **kwargs):
            try:
                return await fn(*args, **kwargs)
            except DoesNotExistInDatabaseException as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                logger.error(f"Unhandled exception: {e}")
                raise HTTPException(status_code=500, detail="Internal Server Error")
            ...

        return _w

    @wraps(fn)
    def _w(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except DoesNotExistInDatabaseException as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

        ...

    return _w
