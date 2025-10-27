from fastapi import APIRouter, HTTPException
from src.component_layer.mosque.component import MosqueComponent
from src.controller_layer.mosque.model import MosqueIn
from src.controller_layer.router_builder import EndpointType, RouterBuilder
from src.logger.logger import logger


class MosqueController:
    def __init__(self, mosque_component: MosqueComponent):
        self.__mosque_component = mosque_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/mosques", ["Mosques"])
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__add_mosque,
            response_model=None,
            summary="Add mosque",
        )
        return router_builder.get_router()

    def __add_mosque(self, mosque_data: MosqueIn):
        try:
            return self.__mosque_component.add_mosque(mosque_data)
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e
