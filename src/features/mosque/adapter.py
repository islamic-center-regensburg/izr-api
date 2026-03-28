from typing import Any
from src.core.db.schemas import PaginatedList
from src.features.mosque.models.schemas import (
    Mosque,
    MosqueCreate,
    MosqueRead,
    MosqueUpdate,
)
from src.features.mosque.models.tables import MosqueTable


class MosqueQueryAdapter:
    def to_query(self, mosque: Mosque | None) -> dict[str, Any]:
        if mosque is None:
            return {}
        return {
            "latitude": mosque.latitude,
            "longitude": mosque.longitude,
            "timezone": mosque.timezone,
        }


class MosqueAdapter:
    @staticmethod
    def to_mosque_read(mosquer_record: MosqueTable) -> MosqueRead:
        return MosqueRead(
            id=mosquer_record.id,
            name=mosquer_record.name,
            address=mosquer_record.address,
            city=mosquer_record.city,
            country=mosquer_record.country,
            latitude=mosquer_record.latitude,
            longitude=mosquer_record.longitude,
            timezone=mosquer_record.timezone,
            prayer_config_id=mosquer_record.prayer_config_id,
        )

    def to_mosques_read(
        self, mosques_records: PaginatedList[MosqueTable]
    ) -> PaginatedList[MosqueRead]:
        return PaginatedList(
            items=[
                self.to_mosque_read(mosque_record)
                for mosque_record in mosques_records.items
            ],
            total=mosques_records.total,
            page=mosques_records.page,
            size=mosques_records.size,
        )

    def from_mosque_create(self, mosque_create: MosqueCreate) -> MosqueTable:
        return MosqueTable(
            name=mosque_create.name,
            address=mosque_create.address,
            city=mosque_create.city,
            country=mosque_create.country,
            latitude=mosque_create.latitude,
            longitude=mosque_create.longitude,
            timezone=mosque_create.timezone,
        )

    def from_mosque_update(
        self, mosque_update: MosqueUpdate, existing_record: MosqueTable
    ) -> MosqueTable:
        return MosqueTable(
            id=existing_record.id,
            name=mosque_update.name or existing_record.name,
            address=mosque_update.address or existing_record.address,
            city=mosque_update.city or existing_record.city,
            country=mosque_update.country or existing_record.country,
            latitude=mosque_update.latitude or existing_record.latitude,
            longitude=mosque_update.longitude or existing_record.longitude,
            timezone=mosque_update.timezone or existing_record.timezone,
            prayer_config_id=mosque_update.prayer_config_id
            or existing_record.prayer_config_id,
        )
