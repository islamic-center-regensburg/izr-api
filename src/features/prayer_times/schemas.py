from datetime import date
from pydantic import model_validator
from sqlmodel import SQLModel, Field
from typing import Optional

from src.core.logging.logger import logger
from src.features.prayer_config.enums import (
    CalculationMethod,
)
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
    day: Optional[int] = Field(default=None, ge=1, le=31, description="Filter by day")
    month: Optional[int] = Field(
        default=None, ge=1, le=12, description="Filter by month"
    )
    year: int = Field(..., ge=1900, le=2999, description="Filter by year")
    hijri: bool = Field(
        default=False, description="Whether to use Hijri calendar for filtering"
    )

    @model_validator(mode="after")
    def validate_date_parts(self) -> "PrayerTimesFilter":
        logger.debug("Validating PrayerTimesFilter date parts")
        if self.month is not None and self.year is None:
            raise ValueError("Invalid filter: 'month' requires 'year'.")
        if self.day is not None and (self.year is None or self.month is None):
            raise ValueError("Invalid filter: 'day' requires both 'year' and 'month'.")

        return self


class PrayerTimesTimingsParams(PrayerTimesFilter):
    latitude: float = Field(49.0134, description="Latitude of the location")
    longitude: float = Field(12.1016, description="Longitude of the location")
    timezone: str = Field(default="UTC", description="Timezone of the location")
    hijri_adjustment: int = Field(
        default=0, ge=-2, le=2, description="Hijri date adjustment"
    )
    method: CalculationMethod = Field(
        default=CalculationMethod.MWL, description="Calculation method"
    )


class PrayerTimesCalendarParams(PrayerTimesTimingsParams):
    pass
