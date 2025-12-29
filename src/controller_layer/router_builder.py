from collections.abc import Callable
from enum import Enum, IntEnum
from typing import Any

from fastapi import APIRouter

from src.controller_layer.api_router_factory import create_default_router


class EndpointType(IntEnum):
    NONE = 0b00000
    GET = 0b00001
    LIST = 0b00010
    CREATE = 0b00100
    DELETE = 0b01000
    UPDATE = 0b10000
    ALL = 0b11111


class RouterBuilder:
    def __init__(self, prefix: str, tags: list[str | Enum]):
        self.__router = create_default_router(prefix, tags)

    def add_method(
        self,
        path: str,
        *,
        endpoint_type: EndpointType,
        endpoint: Callable[..., Any],
        response_model: Any,
        summary: str,
        response_model_exclude_none: bool = False,
    ):
        self.__router.add_api_route(
            path,
            endpoint=endpoint,
            operation_id=endpoint.__name__.replace("__", ""),
            methods=[self.__get_method(endpoint_type)],
            response_model=response_model,
            summary=summary,
            response_model_exclude_none=response_model_exclude_none,
        )

    def get_router(self) -> APIRouter:
        return self.__router

    def __get_method(self, endpoint_type: EndpointType) -> str:
        match endpoint_type:
            case EndpointType.LIST:
                return "GET"
            case EndpointType.GET:
                return "GET"
            case EndpointType.CREATE:
                return "POST"
            case EndpointType.DELETE:
                return "DELETE"
            case EndpointType.UPDATE:
                return "PATCH"
            case _:
                msg = f"Unsupported endpoint type: {endpoint_type}"
                raise ValueError(msg)
