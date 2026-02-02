from __future__ import annotations

from typing import List, Protocol

from src.features.prayer_times.schemas import PrayerTimesBase
from src.features.prayer_times_upload.enums import FileTypeEnum

from .csv_parser import PrayerTimesCsvParser

# If you already have an Excel parser, import it here.
# from .excel_parser import PrayerTimesExcelParser


class PrayerTimesParser(Protocol):
    def parse_bytes(self, content: bytes) -> List[PrayerTimesBase]: ...


class PrayerTimesParserProvider:
    def __init__(self) -> None:
        self._csv = PrayerTimesCsvParser()
        # self._excel = PrayerTimesExcelParser()

    def get_parser(self, file_type: FileTypeEnum) -> PrayerTimesParser:
        if file_type == FileTypeEnum.CSV:
            return self._csv

        if file_type == FileTypeEnum.XLS:
            # return self._excel
            raise NotImplementedError("Excel parser not wired yet")

        raise ValueError(
            f"Unsupported file type for {file_type!r}. Expected .csv, .xls, or .xlsx"
        )
