from fastapi import APIRouter, Body, Depends

from src.core.exceptions import guard
from src.core.router.router_builder import EndpointType, RouterBuilder
from src.features.event.component import EventComponent
from src.features.event.schemas import (
    EventCreate,
    EventFilter,
    EventListOut,
    EventOut,
    EventPaginationFilter,
    EventRead,
    EventTranslationIn,
    EventTranslationRead,
)
from src.features.event.storage import get_minio_repository
from src.integrations.minio.repository import MinioStorageProvider


class EventController:
    def __init__(self, event_component: EventComponent):
        self.__event_component = event_component

    def get_router(self) -> APIRouter:
        router_builder = RouterBuilder("/events", ["Events"])

        router_builder.add_method(
            "/all/{mosque_id}",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_all_events,
            response_model=EventListOut,
            summary="Get events for mosque",
        )
        router_builder.add_method(
            "/{event_id}",
            endpoint_type=EndpointType.GET,
            endpoint=self.__get_event,
            response_model=EventOut,
            summary="Get event by ID",
        )

        router_builder.add_method(
            "",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__create_event,
            response_model=EventRead,
            summary="Create event",
        )
        router_builder.add_method(
            "/{event_id}/translations",
            endpoint_type=EndpointType.CREATE,
            endpoint=self.__create_translation_for_event,
            response_model=EventTranslationRead,
            summary="Create event translation",
        )

        return router_builder.get_router()

    @guard
    def __get_event(self, event_id: int, filter: EventFilter = Depends()) -> EventOut:
        return self.__event_component.get_event(event_id, filter)

    @guard
    def __get_all_events(
        self, mosque_id: int, filters: EventPaginationFilter = Depends()
    ) -> EventListOut:
        return self.__event_component.get_all_events(mosque_id, filters)

    @guard
    def __create_event(
        self,
        event_create: EventCreate = Depends(),
    ) -> EventRead:
        return self.__event_component.create_event(
            event_create,
        )

    @guard
    def __create_translation_for_event(
        self,
        mosque_id: int,
        event_id: int,
        event_translation_in: EventTranslationIn = Depends(),
        description: str | None = Body(
            None, description="Description of the event translation"
        ),
        minio_repository_provider: MinioStorageProvider = Depends(get_minio_repository),
    ) -> EventTranslationRead:
        return self.__event_component.create_event_translation(
            mosque_id,
            event_id,
            event_translation_in,
            description,
            minio_repository_provider,
        )
