from fastapi import APIRouter, Depends, HTTPException
from src.core.db.pagination import PaginatedResponse
from src.features.mosque.component import MosqueComponent
from src.features.mosque.schemas import MosqueIn, MosqueFilter, MosqueOut, MosqueUpdate
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.core.logging.logger import logger


class MosqueController:
    def __init__(self, mosque_component: MosqueComponent):
        self.__mosque_component = mosque_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/mosques", ["Mosques"])
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.LIST,
            endpoint=self.__get_all_mosques,
            response_model=PaginatedResponse[MosqueOut],
            summary="List all mosques",
        )

        router_builder.add_method(
            "/{mosque_id}",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_by_id,
            response_model=MosqueOut,
            summary="Get mosque by ID",
        )
        router_builder.add_method(
            "/{mosque_id}",
            endpoint_type=EndpointType.UPDATE,
            endpoint=self.__update_mosque,
            response_model=MosqueOut,
            summary="Update mosque by ID",
        )

        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__add_mosque,
            response_model=MosqueOut,
            summary="Add mosque",
        )
        return router_builder.get_router()

    def __get_all_mosques(
        self, filter: MosqueFilter = Depends()
    ) -> PaginatedResponse[MosqueOut]:
        try:
            return self.__mosque_component.get_all_mosques(filter)
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e

    def __get_by_id(self, mosque_id: int) -> MosqueOut:
        try:
            mosque = self.__mosque_component.get_mosque_by_id(mosque_id)
            return mosque
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e

    def __add_mosque(self, mosque_data: MosqueIn) -> MosqueOut:
        try:
            return self.__mosque_component.add_mosque(mosque_data)
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e

    def __update_mosque(self, mosque_id: int, mosque_data: MosqueUpdate) -> MosqueOut:
        try:
            updated_mosque = self.__mosque_component.update_mosque(
                mosque_id, mosque_data
            )
            return updated_mosque
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e
