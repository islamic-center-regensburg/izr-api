from typing import Annotated

from fastapi import APIRouter, Query
from src.core.exceptions import guard
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.features.prayer_times.component import PrayerTimesComponent
from src.features.prayer_times.models.adapter import PrayerTimesAdapter
from src.features.prayer_times.models.schemas import (
    AlAdhanPrayerTimesFilter,
    PrayerTimesFilter,
    PrayerTimesOut,
)


class PrayerTimesController:
    def __init__(self, prayer_times_component: PrayerTimesComponent):
        self.__prayer_times_component = prayer_times_component
        self.__prayer_times_adapter = PrayerTimesAdapter()

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

    @guard
    def __get_prayer_times(self, params: Annotated[AlAdhanPrayerTimesFilter, Query()]):
        return self.__prayer_times_adapter.to_prayer_times_out(
            self.__prayer_times_component.get_prayer_times(params)
        )

    @guard
    def __get_prayer_times_for_mosque(
        self,
        mosque_id: str,
        filters: Annotated[PrayerTimesFilter, Query()],
    ):
        return self.__prayer_times_adapter.to_prayer_times_out(
            self.__prayer_times_component.get_prayer_times_for_mosque(
                mosque_id, filters
            )
        )

    @guard
    def __upload_prayer_times_for_mosque(
        self,
        mosque_id: str,
        prayer_times: list[PrayerTimesOut],
    ):
        pass
