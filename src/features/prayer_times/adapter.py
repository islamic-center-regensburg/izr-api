from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel
from pydantic import RootModel, field_validator

from src.features.prayer_times.schemas import PrayerTimesOut, PrayerTimesTimingsParams


class PrayerTimesTimingsParamsQueryAdapter:
    """
    Adapter utilities for PrayerTimesTimingsParams:
    - Build query params for AlAdhan endpoints
    - Build the {date} path segment for GET /timings/{date}
    - Build calendar endpoint path for /calendar vs /hijriCalendar

    This keeps PrayerTimesTimingsParams as a pure schema (no member functions).
    """

    @staticmethod
    def to_query(params: PrayerTimesTimingsParams | None) -> Dict[str, Any]:
        if params is None:
            return {}
        return {
            "latitude": params.latitude,
            "longitude": params.longitude,
            "timezone": params.timezone,
            "adjustment": params.hijri_adjustment,
            "method": int(params.method),
        }


# --- leaf models ---


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


# --- response model with normalization ---
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


class AlAdhanPrayerTimesAdapter:
    def toPrayerTimesOut(self, response: Dict[str, Any]) -> list[PrayerTimesOut]:
        parsed = AlAdhanResponse.model_validate(response)

        if parsed.code != 200:
            raise ValueError(
                f"Invalid response from AlAdhan API: expected code 200, got {parsed.code}"
            )

        return [self.__convert_item(item) for item in parsed.data]

    def __convert_item(self, item: AlAdhanPrayerTimesItem) -> PrayerTimesOut:
        return PrayerTimesOut(
            fajr=item.timings.Fajr,
            shuruq=item.timings.Sunrise,
            dhuhr=item.timings.Dhuhr,
            asr=item.timings.Asr,
            maghrib=item.timings.Maghrib,
            isha=item.timings.Isha,
            gregorian_date=item.date.gregorian.date,
            hijri_date=item.date.hijri.date,
        )
