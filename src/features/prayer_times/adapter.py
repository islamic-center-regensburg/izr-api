from __future__ import annotations
import aladhan

from src.features.prayer_config.schemas import (
    PrayerTimeConfigurationOut,
)
from src.features.prayer_config.enums import (
    CalculationMethod,
    School,
    MidnightMode,
    LatitudeAdjustmentMethod,
    Shafaq,
)

from datetime import datetime, date
from typing import Any, List

from src.features.prayer_times.schemas import PrayerTimesOut


class AlAdhanParametersAdapter:
    """
    Adapter that converts domain-level PrayerTimeConfigurationOut
    into aladhan.Parameters (infrastructure-level object).
    """

    # ---------- enum mappers ----------

    @staticmethod
    def _map_calculation_method(method: CalculationMethod) -> int:
        # If your enum values already match AlAdhan constants
        return int(method)

    @staticmethod
    def _map_school(school: School):
        return int(school)

    @staticmethod
    def _map_midnight_mode(mode: MidnightMode):
        return int(mode)

    @staticmethod
    def _map_latitude_adjustment_method(method: LatitudeAdjustmentMethod):
        return int(method)

    @staticmethod
    def _map_shafaq(shafaq: Shafaq):
        return int(shafaq)

    # ---------- tune adapter ----------

    @staticmethod
    def _build_tune(cfg: PrayerTimeConfigurationOut) -> aladhan.Tune | None:
        if not cfg.tune:
            return None

        return aladhan.Tune(
            fajr=cfg.fajr_tune or 0,
            dhuhr=cfg.dhuhr_tune or 0,
            asr=cfg.asr_tune or 0,
            maghrib=cfg.maghrib_tune or 0,
            isha=cfg.isha_tune or 0,
            # You can add sunrise/imsak/midnight if you expose them
        )

    # ---------- public API ----------

    @classmethod
    def toAlAdhanParameters(
        self, cfg: PrayerTimeConfigurationOut
    ) -> aladhan.Parameters:
        """
        Build aladhan.Parameters from a PrayerTimeConfigurationOut.
        """
        tune = self._build_tune(cfg)

        return aladhan.Parameters(
            method=self._map_calculation_method(cfg.calculation_method),
            school=self._map_school(cfg.school),
            midnightMode=self._map_midnight_mode(cfg.midnight_mode),
            latitudeAdjustmentMethod=self._map_latitude_adjustment_method(
                cfg.latitude_adjustment_method
            ),
            shafaq=self._map_shafaq(cfg.shafaq),
            tune=tune,
            adjustment=cfg.hijri_adjustment,
        )


class AlAdhanPrayerTimesAdapter:
    """
    Adapts aladhan.py responses (Timings or Calendar) into a list[PrayerTimesOut].
    """

    @staticmethod
    def _parse_gregorian_date(value: Any) -> date:
        """
        AlAdhan typically returns Gregorian date info in meta/date fields.
        We'll try the most common shapes:
          - datetime/date object
          - 'DD-MM-YYYY' or 'YYYY-MM-DD' string
        """
        if isinstance(value, date):
            return value

        if isinstance(value, str):
            # try YYYY-MM-DD first
            for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue

        raise ValueError(f"Unsupported gregorian date format: {value!r}")

    @staticmethod
    def _get(obj: Any, path: str, default: Any = None) -> Any:
        """
        Safe getter for nested dict/object with dot paths.
        Supports:
          - dict access
          - attribute access
        Example: _get(x, "date.gregorian.date")
        """
        cur = obj
        for part in path.split("."):
            if cur is None:
                return default
            if isinstance(cur, dict):
                cur = cur.get(part, default)
            else:
                cur = getattr(cur, part, default)
        return cur

    @classmethod
    def from_timings(cls, timings: Any) -> PrayerTimesOut:
        """
        Convert a single aladhan Timings object to PrayerTimesOut.
        aladhan Timings typically has prayer names as attributes or dict keys.
        date metadata is typically available via `timings.date` or `timings.meta`.
        """
        # timings (prayers)
        fajr = cls._get(timings, "fajr") or cls._get(timings, "Fajr")
        dhuhr = cls._get(timings, "dhuhr") or cls._get(timings, "Dhuhr")
        asr = cls._get(timings, "asr") or cls._get(timings, "Asr")
        maghrib = cls._get(timings, "maghrib") or cls._get(timings, "Maghrib")
        isha = cls._get(timings, "isha") or cls._get(timings, "Isha")

        # date blocks (common in AlAdhan)
        gregorian_date = cls._parse_gregorian_date(
            cls._get(timings, "data.date.gregorian.date", None)
        )

        hijri_date = str(cls._get(timings, "data.date.hijri.date", None))

        return PrayerTimesOut(
            fajr=str(fajr.time),
            dhuhr=str(dhuhr.time),
            asr=str(asr.time),
            maghrib=str(maghrib.time),
            isha=str(isha.time),
            gregorian_date=gregorian_date,
            hijri_date=hijri_date,
        )

    @classmethod
    def from_calendar(cls, calendar: Any) -> List[PrayerTimesOut]:
        """
        Convert aladhan calendar response to a list[PrayerTimesOut].

        aladhan calendar may be:
          - list[Timings]
          - dict[str, list[Timings]] (year calendar)
        """
        items: List[Any] = []

        if isinstance(calendar, list):
            items = calendar
        elif isinstance(calendar, dict):
            # year calendar -> dict of months -> list of timings
            for month_list in calendar.values():
                if isinstance(month_list, list):
                    items.extend(month_list)
        else:
            raise ValueError(f"Unsupported calendar response type: {type(calendar)}")

        return [cls.from_timings(t) for t in items]

    @classmethod
    def adapt(cls, aladhan_response: Any) -> List[PrayerTimesOut]:
        """
        Unified entry point:
          - if response is a Timings-like object -> list with 1 item
          - if response is a calendar -> list of items
        """
        if isinstance(aladhan_response, list) or isinstance(aladhan_response, dict):
            return cls.from_calendar(aladhan_response)
        return [cls.from_timings(aladhan_response)]
