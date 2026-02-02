from __future__ import annotations

from datetime import date
from typing import Any, Union

import httpx

from src.features.mosque.adapter import MosqueQueryAdapter
from src.features.mosque.schemas import MosqueBase
from src.features.prayer_config.adapter import PrayerConfigurationQueryAdapter
from src.features.prayer_config.schemas import PrayerConfiguration
from src.features.prayer_times.adapter import PrayerTimesTimingsParamsQueryAdapter
from src.features.prayer_times.schemas import (
    PrayerTimesCalendarParams,
    PrayerTimesFilter,
    PrayerTimesTimingsParams,
)


DateArg = Union[date, str, int]  # date object, "DD-MM-YYYY", or unix timestamp


def _date_to_path(date_arg: DateArg) -> str:
    if isinstance(date_arg, date):
        return date_arg.strftime("%d-%m-%Y")
    return str(date_arg)


# ---- Client implementation ----


class AlAdhanAPIClientProvider:
    def __init__(
        self,
        base_url: str = "https://api.aladhan.com/v1",
        timeout: float = 15.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(timeout=timeout, base_url=self.base_url, verify=False)

    def close(self) -> None:
        self._http.close()

    def get_timings(
        self,
        *,
        params: PrayerTimesTimingsParams | None = None,
        config: PrayerConfiguration | None = None,
        mosque: MosqueBase | None = None,
        filters: PrayerTimesFilter | None = None,
    ) -> dict[str, Any]:
        """
        GET /timings/{date}
        where {date} is 'DD-MM-YYYY' or unix timestamp.
        """
        data_infos = params if params else filters
        date_path = (
            f"{data_infos.day}-{data_infos.month}-{data_infos.year}"
            if data_infos.year
            else date.today().strftime("%d-%m-%Y")
        )

        query_params: dict[str, Any] = (
            PrayerConfigurationQueryAdapter.to_query(config)
            | PrayerTimesTimingsParamsQueryAdapter.to_query(params)
            | MosqueQueryAdapter.to_query(mosque)
        )

        r = self._http.get(f"/timings/{date_path}", params=query_params)
        r.raise_for_status()
        return r.json()

    def get_calendar(
        self,
        *,
        params: PrayerTimesCalendarParams,
    ) -> dict[str, Any]:
        """
        GET /calendar/{year}/{month} or /hijriCalendar/{year}/{month}
        """
        query_params: dict[str, Any] = PrayerTimesTimingsParamsQueryAdapter.to_query(
            params
        )
        endpoint = "/hijriCalendar" if params.hijri else "/calendar"
        r = self._http.get(
            f"{endpoint}/{params.year}{'/' + str(params.month) if params.month is not None else ''}",
            params=query_params,
        )
        r.raise_for_status()
        return r.json()
