from __future__ import annotations
from fastapi import UploadFile
from sqlmodel import Field, SQLModel
from datetime import UTC, datetime
from pydantic import BaseModel, ConfigDict

from src.core.db.schemas import BaseQueryParams
from src.features.prayer_times.enums import PrayerTimesSource


class PrayerTimesBase(SQLModel):
    fajr: str = Field(description="Time for Fajr prayer")
    shuruq: str = Field(description="Time for Shuruq")
    dhuhr: str = Field(description="Time for Dhuhr prayer")
    asr: str = Field(description="Time for Asr prayer")
    maghrib: str = Field(description="Time for Maghrib prayer")
    isha: str = Field(description="Time for Isha prayer")
    gregorian_date: str = Field(description="Gregorian date for this row")
    hijri_date: str = Field(description="Hijri date for this row")


class PrayerTimesCreate(PrayerTimesBase):
    mosque_id: str = Field(description="ID of the mosque")
    pass


class PrayerTimes(PrayerTimesBase):
    pass


class PrayerTimesOut(PrayerTimesBase):
    pass


## Query params and filters


class PrayerTimesTimingQueryParams(BaseModel):
    year: int | None = Field(
        default=datetime.now(UTC).year, ge=2025, le=2050, description="Filter by year"
    )
    month: int | None = Field(default=None, ge=1, le=12, description="Filter by month")
    day: int | None = Field(default=None, ge=1, le=31, description="Filter by day")


# -- Mosque Specific filters
class PrayerTimesIn(SQLModel):
    file: UploadFile = Field(
        description="CSV or Excel file containing prayer times data"
    )
    year: int = Field(
        ..., description="Year for which the prayer times are being uploaded"
    )
    mosque_id: str = Field(
        ..., description="ID of the mosque for which prayer times are being uploaded"
    )


class PrayerTimesFilter(PrayerTimesTimingQueryParams, BaseQueryParams):
    source: PrayerTimesSource = Field(
        default=PrayerTimesSource.API, description="Filter by source of prayer times"
    )


# -- AlAdhan API specific filters
class AlAdhanQueryParams(SQLModel):
    model_config = ConfigDict(extra="forbid")

    method: int | None = None
    school: int | None = None
    midnightMode: int | None = None
    latitudeAdjustmentMethod: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None
    adjustment: int | None = Field(default=None, ge=-2, le=2)
    shafaq: str | None = None

    fajr: float | None = None
    maghrib: float | None = None
    isha: float | None = None
    calendarMethod: str | None = None
    tune: str | None = None

    latitude: float | None = None
    longitude: float | None = None
    timezone: str | None = None

    imsak_tune: int | None = Field(default=None, ge=-60, le=60)
    fajr_tune: int | None = Field(default=None, ge=-60, le=60)
    sunrise_tune: int | None = Field(default=None, ge=-60, le=60)
    dhuhr_tune: int | None = Field(default=None, ge=-60, le=60)
    asr_tune: int | None = Field(default=None, ge=-60, le=60)
    maghrib_tune: int | None = Field(default=None, ge=-60, le=60)
    isha_tune: int | None = Field(default=None, ge=-60, le=60)
    midnight_tune: int | None = Field(default=None, ge=-60, le=60)


class AlAdhanPrayerTimesFilter(BaseModel):
    timings: PrayerTimesTimingQueryParams
    query_params: AlAdhanQueryParams
