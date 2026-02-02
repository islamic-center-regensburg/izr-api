from __future__ import annotations

import re
from datetime import time
from typing import Mapping


_TIME_RE = re.compile(r"^\s*(\d{1,2}):(\d{2})(?::(\d{2}))?\s*$")


def normalize_time_str(value: object, *, keep_seconds: bool = False) -> str:
    """
    Accepts 'H:MM', 'HH:MM', 'HH:MM:SS' and returns normalized:
      - 'HH:MM' by default
      - 'HH:MM:SS' if keep_seconds=True
    Raises ValueError if invalid.
    """
    if value is None:
        raise ValueError("Time value is required")

    m = _TIME_RE.match(str(value))
    if not m:
        raise ValueError(
            f"Invalid time format {value!r}. Expected HH:MM (or HH:MM:SS)."
        )

    hh = int(m.group(1))
    mm = int(m.group(2))
    ss = int(m.group(3) or 0)

    # validates ranges (hour 0-23, minute 0-59, second 0-59)
    try:
        time(hour=hh, minute=mm, second=ss)
    except ValueError as e:
        raise ValueError(f"Invalid time value {value!r}: {e}") from e

    if keep_seconds:
        return f"{hh:02d}:{mm:02d}:{ss:02d}"
    return f"{hh:02d}:{mm:02d}"


def normalize_hijri_date(value: object) -> str:
    """
    Hijri formats can vary a lot, so only enforce "non-empty string".
    """
    if value is None:
        raise ValueError("Hijri date is required")
    s = str(value).strip()
    if not s:
        raise ValueError("Hijri date is required")
    return s


def hhmm_to_minutes(hhmm: str) -> int:
    """
    Converts 'HH:MM' to minutes since 00:00.
    Assumes already validated/normalized.
    """
    hh, mm = hhmm.split(":")
    return int(hh) * 60 + int(mm)


def validate_prayer_times_order(times: Mapping[str, str]) -> None:
    """
    Validates the typical ordering:
      fajr < shuruq < dhuhr < asr < maghrib < isha

    `times` must contain these keys with 'HH:MM' values.
    """
    required = ("fajr", "shuruq", "dhuhr", "asr", "maghrib", "isha")
    missing = [k for k in required if k not in times]
    if missing:
        raise ValueError(f"Missing prayer time fields for order validation: {missing}")

    values = [hhmm_to_minutes(times[k]) for k in required]
    if not all(values[i] < values[i + 1] for i in range(len(values) - 1)):
        raise ValueError(
            "Invalid prayer time order. Expected fajr < shuruq < dhuhr < asr < maghrib < isha."
        )
