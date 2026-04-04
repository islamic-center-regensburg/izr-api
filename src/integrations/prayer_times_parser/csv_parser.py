from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from typing import List, Sequence

from src.features.prayer_times.models.schemas import PrayerTimesBase


@dataclass(frozen=True)
class ParseError:
    row_number: int
    message: str


class PrayerTimesCsvParser:
    required_headers: Sequence[str] = (
        "gregorian_date",
        "hijri_date",
        "fajr",
        "shuruq",
        "dhuhr",
        "asr",
        "maghrib",
        "isha",
    )

    def parse_bytes(
        self, content: bytes, *, encoding: str = "utf-8"
    ) -> List[PrayerTimesBase]:
        """
        Returns validated rows. Raises ValueError with aggregated errors if invalid.
        """
        text = content.decode(encoding, errors="replace")
        f = io.StringIO(text)

        reader = csv.DictReader(f, delimiter=";")
        if not reader.fieldnames:
            raise ValueError("CSV has no headers")

        missing = [h for h in self.required_headers if h not in reader.fieldnames]
        if missing:
            raise ValueError(
                f"CSV is missing required header(s): {missing}. Found: {reader.fieldnames}"
            )

        rows: List[PrayerTimesBase] = []
        errors: List[ParseError] = []

        # row_number: +2 because DictReader starts after header row (which is line 1)
        for i, raw in enumerate(reader, start=2):
            try:
                rows.append(PrayerTimesBase(**raw))
            except Exception as e:
                raise e

        if errors:
            msg = "Invalid prayer times file:\n" + "\n".join(
                f"- line {err.row_number}: {err.message}" for err in errors
            )
            raise ValueError(msg)

        return rows
