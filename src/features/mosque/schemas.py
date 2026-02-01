from typing import Optional
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


class MosqueTable(MosqueBase, table=True):
    __tablename__ = "mosques"
    id: int | None = Field(default=None, primary_key=True, index=True)


class MosqueIn(MosqueBase):
    pass


class MosqueOut(MosqueBase):
    id: int


class Mosque(MosqueBase):
    id: int


Mosque


class MosqueUpdate(SQLModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None


class MosqueFilter(PageParams):
    name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
