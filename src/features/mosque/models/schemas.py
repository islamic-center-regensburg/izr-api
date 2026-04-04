from typing import Optional
import uuid
from sqlmodel import Field, SQLModel

from src.core.db.schemas import BaseQueryParams, PageParams
from src.core.db.validity import VersionedSQLModel


class Mosque(VersionedSQLModel):
    name: str = Field(index=True, description="Name of the mosque")
    address: str = Field(description="Address of the mosque")
    city: str = Field(description="City where the mosque is located")
    country: str = Field(description="Country where the mosque is located")
    latitude: float = Field(description="Latitude of the mosque location")
    longitude: float = Field(description="Longitude of the mosque location")
    timezone: str = Field(default="UTC", description="Timezone of the mosque location")


class MosqueRead(Mosque):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    prayer_config_id: Optional[uuid.UUID] = Field(
        default=None, description="Active prayer configuration ID for the mosque"
    )

    @classmethod
    def get_business_key_fields(cls):
        pass


class MosqueCreate(Mosque):
    @classmethod
    def get_business_key_fields(cls):
        pass


class MosqueUpdate(SQLModel):
    name: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    prayer_config_id: uuid.UUID | None = None


class MosqueQueryParams(BaseQueryParams, PageParams):
    name: str | None = None
    city: str | None = None
    country: str | None = None
