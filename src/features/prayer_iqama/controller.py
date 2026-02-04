from fastapi import APIRouter, Depends

from src.core.db.pagination import PaginatedResponse
from src.core.exceptions import guard
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.features.prayer_iqama.component import PrayerIqamaComponent
from src.features.prayer_iqama.schemas import (
    PrayerIqamaFilter,
    PrayerIqamaIn,
    PrayerIqamaOut,
    PrayerIqamaUpdate,
)


class PrayerIqamaController:
    def __init__(self, prayer_iqama_component: PrayerIqamaComponent):
        self.__prayer_iqama_component = prayer_iqama_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/prayer_iqama", ["Prayer Iqama"])

        router_builder.add_method(
            "",
            endpoint_type=EndpointType.LIST,
            endpoint=self.__get_all_prayer_iqamas,
            response_model=PaginatedResponse[PrayerIqamaOut],
            summary="Get Prayer Iqamas",
        )
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__create_prayer_iqama,
            response_model=PrayerIqamaOut,
            summary="Create Prayer Iqama",
        )
        router_builder.add_method(
            "/{prayer_iqama_id}",
            endpoint_type=EndpointType.UPDATE,
            endpoint=self.__update_prayer_iqama,
            response_model=PrayerIqamaOut,
            summary="Update Prayer Iqama",
        )

        router_builder.add_method(
            "/{mosque_id}",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_prayer_iqamas_for_mosque,
            response_model=list[PrayerIqamaOut],
            summary="Get Prayer Iqamas for Mosque",
        )

        return router_builder.get_router()

    @guard
    def __get_all_prayer_iqamas(
        self,
        filter: PrayerIqamaFilter = Depends(),
    ) -> PaginatedResponse[PrayerIqamaOut]:
        return self.__prayer_iqama_component.get_prayer_iqamas(filter)

    @guard
    def __get_prayer_iqamas_for_mosque(
        self,
        mosque_id: int,
    ) -> list[PrayerIqamaOut]:
        return self.__prayer_iqama_component.get_prayer_iqamas_for_mosque(mosque_id)

    @guard
    def __create_prayer_iqama(self, prayer_iqama_in: PrayerIqamaIn) -> PrayerIqamaOut:
        return self.__prayer_iqama_component.create_prayer_iqama(prayer_iqama_in)

    @guard
    def __update_prayer_iqama(
        self, prayer_iqama_id: int, prayer_iqama_update: PrayerIqamaUpdate
    ) -> PrayerIqamaOut:
        return self.__prayer_iqama_component.update_prayer_iqama(
            prayer_iqama_id, prayer_iqama_update
        )
