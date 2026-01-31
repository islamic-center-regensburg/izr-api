from sqlmodel import Field, SQLModel


class MosqueTable(SQLModel, table=True):
    __tablename__ = "mosques"  # pyright: ignore [reportAssignmentType]

    id: int = Field(default=None, primary_key=True, index=True)

    name: str = Field(index=True, description="Name of the mosque")
    address: str = Field(description="Address of the mosque")
    city: str = Field(description="City where the mosque is located")
    country: str = Field(description="Country where the mosque is located")
    latitude: float = Field(description="Latitude of the mosque location")
    longitude: float = Field(description="Longitude of the mosque location")
    timezone: str = Field(default="UTC", description="Timezone of the mosque location")
