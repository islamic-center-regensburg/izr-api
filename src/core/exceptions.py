from __future__ import annotations

from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError as CoreValidationError

from src.core.logging.logger import logger

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


def guard(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def _w(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return fn(*args, **kwargs)

        # let already-well-formed HTTP errors pass
        except HTTPException:
            raise

        # hardcoded exceptions you expect
        except ValueError as e:
            logger.error("Internal server error", e)
            raise HTTPException(status_code=400, detail=str(e))

        # add more here as you wish
        # except IntegrityError:
        #     raise HTTPException(status_code=409, detail="Conflict")

        # fallback
        except Exception as e:
            logger.error("Internal server error", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    return _w
