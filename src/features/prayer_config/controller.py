from fastapi import APIRouter, Depends
from src.core.db.pagination import PaginatedResponse
from src.core.exceptions import guard
from src.features.prayer_config.component import PrayerConfigComponent
from src.features.prayer_config.enums import CalculationMethod
from src.features.prayer_config.schemas import (
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
            endpoint=self.__get_all_configs,
            response_model=PaginatedResponse[PrayerConfigurationOut],
            summary="List prayer configurations",
        )
        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__add_prayer_configuration,
            response_model=PrayerConfigurationOut,
            summary="Add prayer configuration",
        )

        router_builder.add_method(
            "/{prayer_config_id}",
            endpoint_type=EndpointType.UPDATE,
            endpoint=self.__update_prayer_configuration,
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
    def __get_all_configs(
        self, filter: PrayerConfigurationFilter = Depends()
    ) -> PaginatedResponse[PrayerConfigurationOut]:
        return self.__prayer_config_component.get_all_prayer_configurations(filter)

    @guard
    def __add_prayer_configuration(
        self, mosque_id: int, config_data: PrayerConfigurationIn
    ) -> PrayerConfigurationOut:
        return self.__prayer_config_component.add_prayer_configuration(
            mosque_id, config_data
        )

    @guard
    def __update_prayer_configuration(
        self, prayer_config_id: int, config_data: PrayerTimeConfigurationUpdate
    ) -> PrayerConfigurationOut:
        return self.__prayer_config_component.update_prayer_configuration(
            prayer_config_id, config_data
        )

    @guard
    def __get_calculation_methods(self) -> dict[int, str]:
        return CalculationMethod.labels()
