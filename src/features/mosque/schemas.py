from typing import Optional
import uuid
from uuid import UUID
from sqlmodel import SQLModel, Field

from src.core.db.pagination import PageParams


class MosqueBase(SQLModel):
    name: str = Field(index=True, description="Name of the mosque")
    address: str = Field(description="Address of the mosque")
    city: str = Field(description="City where the mosque is located")
    country: str = Field(description="Country where the mosque is located")
    latitude: float = Field(description="Latitude of the mosque location")
    longitude: float = Field(description="Longitude of the mosque location")
    timezone: str = Field(default="UTC", description="Timezone of the mosque location")
    prayer_config_id: Optional[int] = Field(
        default=None, description="Active prayer configuration ID for the mosque"
    )


class MosqueTable(MosqueBase, table=True):
    __tablename__ = "mosques"
    id: UUID | None = Field(default_factory=uuid.uuid4, primary_key=True, index=True)


class MosqueIn(MosqueBase):
    pass


class MosqueOut(MosqueBase):
    id: UUID


class Mosque(MosqueBase):
    id: UUID


Mosque


class MosqueUpdate(SQLModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None
    prayer_config_id: Optional[int] = None


class MosqueFilter(PageParams):
    name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
