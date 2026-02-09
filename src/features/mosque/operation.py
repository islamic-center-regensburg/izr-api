from uuid import UUID
from src.core.db.pagination import PaginationBuilder
from src.core.db.filters import Filter, Operator
from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.features.mosque.schemas import MosqueFilter, MosqueTable


class MosqueOperation:
    def __init__(self, db_repository_provider: DatabaseRepositoryProvider):
        self.db_repository = db_repository_provider

    def get_all_mosques(self, filter: MosqueFilter):
        filters = [
            Filter(attribute="name", value=filter.name, operator=Operator.EQ),
            Filter(attribute="city", value=filter.city, operator=Operator.EQ),
            Filter(attribute="country", value=filter.country, operator=Operator.EQ),
        ]
        with self.db_repository.get_database_repository() as db:
            data = db.get_all(
                MosqueTable, filters=filters, limit=filter.limit, offset=filter.offset
            )
            total = db.count(MosqueTable, filters=filters)
            return PaginationBuilder.build(
                items=data,
                total=total,
                page=filter.page,
                size=filter.size,
            )

    def get_mosque_by_id(self, mosque_id: str):
        with self.db_repository.get_database_repository() as db:
            mosque = db.get_by_id(MosqueTable, mosque_id)
            return mosque

    def add_mosque(self, mosque_data):
        with self.db_repository.get_database_repository() as db:
            mosque_record = MosqueTable(
                name=mosque_data.name,
                address=mosque_data.address,
                latitude=mosque_data.latitude,
                longitude=mosque_data.longitude,
                city=mosque_data.city,
                country=mosque_data.country,
                timezone=mosque_data.timezone,
            )
            mosque = db.create(mosque_record)
            return mosque

    def update_mosque(self, mosque_id: UUID, mosque_data):
        with self.db_repository.get_database_repository() as db:
            mosque = db.get_by_id(MosqueTable, mosque_id)
            if mosque is None:
                return None

            for key, value in mosque_data.dict(exclude_unset=True).items():
                setattr(mosque, key, value)

            updated_mosque = db.update(mosque)
            return updated_mosque
