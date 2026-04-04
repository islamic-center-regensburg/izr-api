from typing import Protocol
from uuid import UUID
from src.core.db.order_by import OrderByAdapter
from src.core.db.schemas import PaginationBuilder
from src.core.db.filters import Filter, Operator
from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.mosque.adapter import MosqueAdapter
from src.features.mosque.models.schemas import MosqueQueryParams, MosqueUpdate
from src.features.mosque.models.tables import MosqueTable


class MosqueOperationInterface(Protocol):
    def find(self, query: MosqueQueryParams): ...
    def get(self, mosque_id: str): ...
    def create(self, mosque_data): ...
    def update(self, mosque_id: UUID, mosque_data): ...


class MosqueOperation(MosqueOperationInterface):
    def __init__(self, db_repository_provider: DatabaseRepositoryProvider):
        self.__db_repository = db_repository_provider
        self.__mosque_adapter = MosqueAdapter()
        self.__order_by_adapter = OrderByAdapter()

    def find(self, query: MosqueQueryParams):
        filters = Filter.get_validity_filters(query.valid_at)
        filters.extend(
            [
                Filter(attribute="name", value=query.name, operator=Operator.EQ),
                Filter(attribute="city", value=query.city, operator=Operator.EQ),
                Filter(attribute="country", value=query.country, operator=Operator.EQ),
            ]
        )

        order_by = self.__order_by_adapter.from_sort_strings(query.sort or [])
        with self.__db_repository.get_database_repository() as db:
            records = db.get_all(
                MosqueTable,
                filters=filters,
                limit=query.limit,
                offset=query.offset,
                order_by=order_by,
            )
            total = db.count(MosqueTable, filters=filters)
            return PaginationBuilder.build(
                items=records,
                total=total,
                page=query.page,
                size=query.size,
            )

    def get(self, mosque_id: str):
        with self.__db_repository.get_database_repository() as db:
            record = db.get_by_id(MosqueTable, mosque_id)
            return record

    def create(self, mosque_data):
        with self.__db_repository.get_database_repository() as db:
            record = db.create(self.__mosque_adapter.from_mosque_create(mosque_data))
            return record

    def update(self, mosque_id: UUID, mosque_update: MosqueUpdate):
        with self.__db_repository.get_database_repository() as db:
            existing_record = db.get_by_id(MosqueTable, mosque_id)
            updated_record = db.update(
                self.__mosque_adapter.from_mosque_update(mosque_update, existing_record)
            )
            return updated_record
