import uuid
from sqlmodel import Field

from src.core.db.validity import VersionedSQLModel


class PrayerTimesTable(VersionedSQLModel, table=True):
    __tablename__ = "prayer_times"
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
    )
    fajr: str = Field(...)
    shuruq: str = Field(...)
    dhuhr: str = Field(...)
    asr: str = Field(...)
    maghrib: str = Field(...)
    isha: str = Field(...)

    gregorian_date: str = Field(...)
    hijri_date: str = Field(...)
    mosque_id: str = Field(...)

    year: int = Field(...)
    month: int = Field(...)
    day: int = Field(...)

    mosque_id: uuid.UUID = Field(foreign_key="mosques.id", index=True)

    @classmethod
    def get_business_key_fields(cls) -> set[str]:
        return {"gregorian_date"}
