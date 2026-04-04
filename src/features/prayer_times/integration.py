from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal, Dict, List

import httpx

from pydantic import RootModel, field_validator, BaseModel

from src.features.prayer_times.models.schemas import AlAdhanQueryParams


class AlAdhanCalendarType(StrEnum):
    ANNUAL: Literal["annual"] = "annual"
    MONTHLY: Literal["monthly"] = "monthly"
    DAILY: Literal["daily"] = "daily"


class AlAdhanPrayerTimesParams(BaseModel):
    calendar: AlAdhanCalendarType
    year: int
    month: int | None = None
    day: int | None = None
    query_params: AlAdhanQueryParams


class AlAdhanTimings(BaseModel):
    Fajr: str
    Sunrise: str
    Dhuhr: str
    Asr: str
    Maghrib: str
    Isha: str

    @field_validator(
        "Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha", mode="before"
    )
    @classmethod
    def validate_timing_format(cls, v: str) -> str:
        if isinstance(v, str):
            return v.split(" ")[0]
        raise ValueError("Invalid timing format")


class AlAdhanGregorian(BaseModel):
    date: str  # "01-01-2026"


class AlAdhanHijri(BaseModel):
    date: str


class AlAdhanDate(BaseModel):
    gregorian: AlAdhanGregorian
    hijri: AlAdhanHijri


class AlAdhanPrayerTimesItem(BaseModel):
    timings: AlAdhanTimings
    date: AlAdhanDate


class AlAdhanMonthlyData(RootModel[Dict[str, List[AlAdhanPrayerTimesItem]]]):
    pass


class AlAdhanResponse(BaseModel):
    code: int
    data: List[AlAdhanPrayerTimesItem]

    @field_validator("data", mode="before")
    @classmethod
    def normalize_data(cls, v: Any):
        # daily/object: {"timings":..., "date":...}
        if isinstance(v, dict) and "timings" in v and "date" in v:
            return [v]

        # monthly/ list: [{...}, {...}]
        if isinstance(v, list):
            return v

        # annual: {"1":[{...}], "2":[{...}], ...}
        if isinstance(v, dict):
            monthly = AlAdhanMonthlyData.model_validate(v).root
            flattened: list[dict] = []
            for day_items in monthly.values():
                flattened.extend(day_items)
            return flattened

        raise ValueError("Unexpected response format for 'data'")


class AlAdhanAPIClientProvider:
    def __init__(
        self,
        base_url: str = "https://api.aladhan.com/v1",
        timeout: float = 15.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(timeout=timeout, base_url=self.base_url, verify=False)

    def get_prayer_times(self, params: AlAdhanPrayerTimesParams) -> AlAdhanResponse:
        """
        GET /calendar/{year}/{month} or /hijriCalendar/{year}/{month}
        """
        if params.calendar == AlAdhanCalendarType.DAILY:
            date = datetime(
                year=params.year,
                month=params.month,
                day=params.day,
            )
            return self.__get_date_prayer_times(date, params.query_params)

        date_path = f"{params.year}"
        if params.month is not None:
            date_path += f"/{params.month}"

        r = self._http.get(
            f"/calendar/{date_path}",
            params=params.query_params.model_dump(exclude_none=True),
        )
        r.raise_for_status()
        return AlAdhanResponse.model_validate(r.json())

    def __get_date_prayer_times(
        self,
        date: datetime,
        query_params: AlAdhanQueryParams,
    ) -> AlAdhanResponse:
        """
        GET /timings/{date}
        where {date} is 'DD-MM-YYYY' or unix timestamp.
        """
        timings_date = date.strftime("%d-%m-%Y")
        r = self._http.get(
            f"/timings/{timings_date}",
            params=query_params.model_dump(exclude_none=True),
        )
        r.raise_for_status()
        return AlAdhanResponse.model_validate(r.json())
