from src.core.db.database_repository_provider import DatabaseRepositoryProvider

from src.core.db.filters import Filter, Operator
from src.core.db.pagination import PaginationBuilder
from src.features.event.schemas import (
    EventPaginationFilter,
    EventRead,
    EventTranslationIn,
    EventTranslationRead,
    EventTranslationTable,
)
from src.features.event.schemas import (
    EventFilter,
    EventCreate,
    EventListOut,
    EventOut,
    EventTable,
)


class EventOperation:
    def __init__(self, db_repository_provider: DatabaseRepositoryProvider):
        self.__db_repository_provider = db_repository_provider

    def get_event_by_id(self, event_id: int, filter: EventFilter) -> EventOut:
        with self.__db_repository_provider.get_database_repository() as db:
            filters = [
                Filter(attribute="id", value=event_id, operator=Operator.EQ),
                Filter(
                    attribute="valid_to", value=filter.date_from, operator=Operator.LE
                ),
            ]
            event_records: list[EventRead] = db.get_all(EventTable, filters=filters)
            event = event_records[0]

            filters = [
                Filter(attribute="event_id", value=event.id, operator=Operator.EQ),
                Filter(
                    attribute="language", value=filter.language, operator=Operator.EQ
                ),
            ]
            event_translation_records: list[EventTranslationRead] = db.get_all(
                EventTranslationTable, filters=filters
            )

            return EventOut(
                id=event.id,
                mosque_id=event.mosque_id,
                created_at=event.created_at,
                updated_at=event.updated_at,
                valid_to=event.valid_to,
                translations=event_translation_records,
            )

    def get_all_events(
        self, mosque_id: int, filter: EventPaginationFilter
    ) -> EventListOut:
        with self.__db_repository_provider.get_database_repository() as db:
            events = []

            filters = [
                Filter(attribute="mosque_id", value=mosque_id, operator=Operator.EQ),
                Filter(
                    attribute="valid_to", value=filter.date_from, operator=Operator.LE
                ),
            ]
            event_records: list[EventRead] = db.get_all(EventTable, filters=filters)
            for event in event_records:
                filters = [
                    Filter(attribute="event_id", value=event.id, operator=Operator.EQ),
                    Filter(
                        attribute="language",
                        value=filter.language,
                        operator=Operator.EQ,
                    ),
                ]
                event_translation_records: list[EventTranslationRead] = db.get_all(
                    EventTranslationTable, filters=filters
                )

                events.append(
                    EventOut(
                        id=event.id,
                        mosque_id=event.mosque_id,
                        created_at=event.created_at,
                        updated_at=event.updated_at,
                        valid_to=event.valid_to,
                        translations=event_translation_records,
                    )
                )
            return PaginationBuilder.build(
                items=events, total=len(events), size=filter.size, page=filter.page
            )

    def create(
        self,
        event_create: EventCreate,
    ) -> EventRead:
        with self.__db_repository_provider.get_database_repository() as db:
            event_record = db.create(
                EventTable(
                    mosque_id=event_create.mosque_id, valid_to=event_create.valid_to
                )
            )

            return event_record

    def create_event_translation(
        self,
        event_id: int,
        event_translation_in: EventTranslationIn,
        storage_dir_path: str | None = None,
    ) -> EventTranslationRead:
        with self.__db_repository_provider.get_database_repository() as db:
            event_translation_record = db.create(
                EventTranslationTable(
                    event_id=event_id,
                    title=event_translation_in.title,
                    description=event_translation_in.description,
                    language=event_translation_in.language,
                    media=storage_dir_path,
                )
            )

            return event_translation_record
