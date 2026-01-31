from datetime import date
from sqlmodel import SQLModel, Field
from typing import Optional

from src.features.prayer_config.enums import CalculationMethod
from src.features.prayer_times.enums import PrayerTimesSource


class PrayerTimesBase(SQLModel):
    fajr: str = Field(..., description="Time for Fajr prayer")
    dhuhr: str = Field(..., description="Time for Dhuhr prayer")
    asr: str = Field(..., description="Time for Asr prayer")
    maghrib: str = Field(..., description="Time for Maghrib prayer")
    isha: str = Field(..., description="Time for Isha prayer")

    gregorian_date: date = Field(..., description="Gregorian date for this row")
    hijri_date: str = Field(..., description="Hijri date for this row")


class PrayerTimesTable(PrayerTimesBase, table=True):
    __tablename__ = "prayer_times"

    id: Optional[int] = Field(default=None, primary_key=True)
    mosque_id: int = Field(foreign_key="mosques.id", index=True)

    upload_id: Optional[int] = Field(
        default=None, foreign_key="prayer_time_uploads.id", index=True
    )


class PrayerTimesOut(PrayerTimesBase):
    pass


class PrayerTimesSourceParams(SQLModel):
    source: PrayerTimesSource = Field(
        default=PrayerTimesSource.API,
        description="Where to load prayer times from: auto|stored|api",
    )


class PrayerTimesFilter(SQLModel):
    day: Optional[date] = Field(date.today(), description="Filter by day")
    year: Optional[int] = Field(None, ge=1900, le=2999, description="Filter by year")
    month: Optional[int] = Field(None, ge=1, le=12, description="Filter by month")


class PrayerTimesGenericParams(SQLModel):
    latitude: float = Field(49.013432, description="Latitude of the location")
    longitude: float = Field(12.101624, description="Longitude of the location")
    timezone: str = Field("UTC", description="Timezone of the location")
    hijri_adjustment: int = Field(0, le=2, ge=-2, description="Hijri date adjustment")
    method: CalculationMethod = Field(
        default=CalculationMethod.MWL,
        description="Calculation method for prayer times",
    )
