from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query
from src.core.db.schemas import PaginatedList
from src.core.exceptions import guard
from src.features.mosque.component import MosqueComponent
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.features.mosque.models.schemas import (
    MosqueCreate,
    MosqueQueryParams,
    MosqueRead,
    MosqueUpdate,
)


class MosqueController:
    def __init__(self, mosque_component: MosqueComponent):
        self.__mosque_component = mosque_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/mosques", ["Mosques"])
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.LIST,
            endpoint=self.__get_all_mosques,
            response_model=PaginatedList[MosqueRead],
            summary="List all mosques",
        )

        router_builder.add_method(
            "/{mosque_id}",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_mosque_by_id,
            response_model=MosqueRead,
            summary="Get mosque by ID",
        )
        router_builder.add_method(
            "/{mosque_id}",
            endpoint_type=EndpointType.UPDATE,
            endpoint=self.__update_mosque,
            response_model=MosqueRead,
            summary="Update mosque by ID",
        )

        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__add_mosque,
            response_model=MosqueRead,
            summary="Add mosque",
        )
        return router_builder.get_router()

    def __get_all_mosques(
        self, query: Annotated[MosqueQueryParams, Query()]
    ) -> PaginatedList[MosqueRead]:
        return self.__mosque_component.get_all_mosques(query)

    @guard
    def __get_mosque_by_id(self, mosque_id: UUID) -> MosqueRead:
        return self.__mosque_component.get_mosque_by_id(mosque_id)

    def __add_mosque(self, mosque_data: MosqueCreate) -> MosqueRead:
        return self.__mosque_component.add_mosque(mosque_data)

    def __update_mosque(self, mosque_id: UUID, mosque_data: MosqueUpdate) -> MosqueRead:
        return self.__mosque_component.update_mosque(mosque_id, mosque_data)
