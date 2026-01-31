from __future__ import annotations

from datetime import date as dt_date
from typing import Optional, Union, Any

import aladhan


class AlAdhanAPIClientProvider:
    def __init__(self) -> None:
        self.__client: Optional[aladhan.Client] = None

    def get_client(self) -> aladhan.Client:
        if self.__client is None:
            self.__client = aladhan.Client()
        return self.__client

    def get_timings(
        self,
        *,
        latitude: float,
        longitude: float,
        day: Union[dt_date, str, int],
        params: Optional[aladhan.Parameters] = None,
    ) -> aladhan.Timings:
        """
        Day timings by coordinates.
        day: datetime.date OR 'DD-MM-YYYY' OR unix timestamp.
        """
        client = self.get_client()
        date_arg = day.strftime("%d-%m-%Y") if isinstance(day, dt_date) else day
        return client.get_timings(
            latitude=latitude,
            longitude=longitude,
            date=aladhan.TimingsDateArg(date_arg),
            params=params or aladhan.Parameters(),
        )

    def get_calendar(
        self,
        *,
        latitude: float,
        longitude: float,
        year: int,
        month: Optional[int] = None,
        hijri: bool = False,
        params: Optional[aladhan.Parameters] = None,
    ) -> Any:
        """
        Calendar timings by coordinates.
        - month provided -> month calendar
        - month None -> full year calendar
        """
        client = self.get_client()
        date_arg = aladhan.CalendarDateArg(year=year, month=month or 1, hijri=hijri)
        return client.get_calendar(
            latitude=latitude,
            longitude=longitude,
            date=date_arg,
            params=params or aladhan.Parameters(),
        )
