import uuid

from sqlmodel import Field

from src.core.db.validity import VersionedSQLModel


class MosqueTable(VersionedSQLModel, table=True):
    __tablename__ = "mosques"
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    name: str = Field(index=True, description="Name of the mosque")
    address: str = Field(description="Address of the mosque")
    city: str = Field(description="City where the mosque is located")
    country: str = Field(description="Country where the mosque is located")
    latitude: float = Field(description="Latitude of the mosque location")
    longitude: float = Field(description="Longitude of the mosque location")
    timezone: str = Field(default="UTC", description="Timezone of the mosque location")
    prayer_config_id: uuid.UUID | None = Field(
        default=None, description="Active prayer configuration ID for the mosque"
    )

    @classmethod
    def get_business_key_fields(cls):
        return {"name"}
