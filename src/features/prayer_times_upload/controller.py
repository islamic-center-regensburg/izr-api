from fastapi import APIRouter, Depends, HTTPException
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.features.prayer_times_upload.component import PrayerTimesUploadComponent
from src.features.prayer_times_upload.dependencies import (
    get_minio_repository,
    get_prayer_times_parser_repository,
)
from src.features.prayer_times_upload.schemas import (
    PrayerTimeUploadIn,
    PrayerTimeUploadOut,
)
from src.integrations.minio.repository import MinioStorageProvider
from src.integrations.prayer_times_parser.repository import PrayerTimesParserProvider


class PrayerTimesUploadController:
    def __init__(self, prayer_times_upload_component: PrayerTimesUploadComponent):
        self.__prayer_times_upload_component = prayer_times_upload_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/prayer_times_upload", ["Prayer Times Upload"])

        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__upload_prayer_times,
            response_model=PrayerTimeUploadOut,
            summary="Upload Prayer Times",
        )
        return router_builder.get_router()

    def __upload_prayer_times(
        self,
        prayer_times_parser_provider: PrayerTimesParserProvider = Depends(
            get_prayer_times_parser_repository
        ),
        minio_provider: MinioStorageProvider = Depends(get_minio_repository),
        prayer_time_upload_in: PrayerTimeUploadIn = Depends(),
    ) -> PrayerTimeUploadOut:
        try:
            return self.__prayer_times_upload_component.upload_prayer_times(
                prayer_time_upload_in,
                minio_provider,
                prayer_times_parser_provider,
            )
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve)) from ve
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error") from e
