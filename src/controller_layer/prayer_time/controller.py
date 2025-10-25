from fastapi import APIRouter, HTTPException
from src.component_layer.prayer_time.component import PrayerTimeComponent
from src.controller_layer.router_builder import EndpointType, RouterBuilder
from src.logger.logger import logger
from aladhan import Adhan


class PrayerTimeController:
    def __init__(self, prayer_time_component: PrayerTimeComponent):
        self.__prayer_time_component = prayer_time_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/prayer_times", ["Prayer Times"])
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.LIST,
            endpoint=self.__get_today_prayer_times,
            response_model=None,
            summary="List prayer times",
        )
        return router_builder.get_router()

    def __get_today_prayer_times(self, mosque_id: str) -> list[Adhan]:
        try:
            return self.__prayer_time_component.get_today_prayer_times_for_mosque(
                mosque_id
            )
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e
