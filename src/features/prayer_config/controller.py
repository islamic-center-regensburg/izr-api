from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from src.core.db.schemas import PaginatedList
from src.core.exceptions import guard
from src.features.prayer_config.component import PrayerConfigComponent
from src.features.prayer_config.enums import CalculationMethod
from src.features.prayer_config.schemas import (
    CalcMethodLanguage,
    PrayerConfigurationFilter,
    PrayerConfigurationIn,
    PrayerConfigurationOut,
    PrayerTimeConfigurationUpdate,
)
from src.core.router.router_builder import EndpointType, RouterBuilder


class PrayerConfigController:
    def __init__(self, prayer_config_component: PrayerConfigComponent):
        self.__prayer_config_component = prayer_config_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/prayer_configs", ["Prayer Configurations"])
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.LIST,
            endpoint=self.__get_all_prayer_configs,
            response_model=PaginatedList[PrayerConfigurationOut],
            summary="List prayer configurations",
        )
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__add_prayer_config,
            response_model=PrayerConfigurationOut,
            summary="Add prayer configuration",
        )

        router_builder.add_method(
            "/{prayer_config_id}",
            endpoint_type=EndpointType.UPDATE,
            endpoint=self.__update_prayer_config,
            response_model=PrayerConfigurationOut,
            summary="Update prayer configuration",
        )

        router_builder.add_method(
            "/calculation_methods",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_calculation_methods,
            response_model=dict[int, str],
            summary="Calculation Methods",
        )
        return router_builder.get_router()

    @guard
    def __get_all_prayer_configs(
        self, filter: Annotated[PrayerConfigurationFilter, Query()]
    ) -> PaginatedList[PrayerConfigurationOut]:
        return self.__prayer_config_component.get_all_prayer_configurations(filter)

    @guard
    def __add_prayer_config(
        self, mosque_id: UUID, config_data: PrayerConfigurationIn
    ) -> PrayerConfigurationOut:
        return self.__prayer_config_component.add_prayer_configuration(
            mosque_id, config_data
        )

    @guard
    def __update_prayer_config(
        self, prayer_config_id: UUID, config_data: PrayerTimeConfigurationUpdate
    ) -> PrayerConfigurationOut:
        return self.__prayer_config_component.update_prayer_configuration(
            prayer_config_id, config_data
        )

    @guard
    def __get_calculation_methods(
        self, language: CalcMethodLanguage = Depends()
    ) -> dict[int, str]:
        return CalculationMethod.labels(language.lang)
