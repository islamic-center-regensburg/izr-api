from fastapi import APIRouter, Depends, HTTPException
from src.core.db.pagination import PaginatedResponse
from src.features.prayer_config.component import PrayerConfigComponent
from src.features.prayer_config.enums import CalculationMethod
from src.features.prayer_config.schemas import (
    PrayerConfigurationFilter,
    PrayerConfigurationIn,
    PrayerConfigurationOut,
    PrayerTimeConfigurationUpdate,
)
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.core.logging.logger import logger


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

    def __get_all_configs(
        self, filter: PrayerConfigurationFilter = Depends()
    ) -> PaginatedResponse[PrayerConfigurationOut]:
        try:
            return self.__prayer_config_component.get_all_prayer_configurations(filter)
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e

    def __add_prayer_configuration(
        self, mosque_id: str, config_data: PrayerConfigurationIn
    ) -> PrayerConfigurationOut:
        try:
            return self.__prayer_config_component.add_prayer_configuration(
                mosque_id, config_data
            )
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e

    def __update_prayer_configuration(
        self, prayer_config_id: str, config_data: PrayerTimeConfigurationUpdate
    ) -> PrayerConfigurationOut:
        try:
            return self.__prayer_config_component.update_prayer_configuration(
                prayer_config_id, config_data
            )
        except Exception as e:
            logger.error("Internal server error", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error") from e

    def __get_calculation_methods(self) -> dict[int, str]:
        return CalculationMethod.labels()
