from fastapi import APIRouter, Depends, HTTPException
from src.core.logging.logger import logger
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.features.prayer_times.component import PrayerTimesComponent
from src.features.prayer_times.schemas import (
    PrayerTimesFilter,
    PrayerTimesOut,
    PrayerTimesSourceParams,
    PrayerTimesTimingsParams,
)


class PrayerTimesController:
    def __init__(self, prayer_times_component: PrayerTimesComponent):
        self.__prayer_times_component = prayer_times_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/prayer_times", ["Prayer Times"])
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.LIST,
            endpoint=self.__get_prayer_times,
            response_model=list[PrayerTimesOut],
            summary="Get Prayer Times",
        )

        router_builder.add_method(
            "/{mosque_id}",
            endpoint_type=EndpointType.LIST,
            response_model=list[PrayerTimesOut],
            endpoint=self.__get_prayer_times_for_mosque,
            summary="Get Prayer Times for a specific mosque",
        )

        return router_builder.get_router()

    def __get_prayer_times(self, params: PrayerTimesTimingsParams = Depends()):
        try:
            return self.__prayer_times_component.get_prayer_times(params)
        except Exception:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")

    def __get_prayer_times_for_mosque(
        self,
        mosque_id: int,
        source: PrayerTimesSourceParams = Depends(),
        filters: PrayerTimesFilter = Depends(),
    ):
        try:
            return self.__prayer_times_component.get_prayer_times_for_mosque(
                mosque_id, source, filters
            )
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e
