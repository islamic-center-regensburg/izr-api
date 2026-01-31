from enum import StrEnum


class PrayerTimesSource(StrEnum):
    API = "api"  # only AlAdhan (mosque config)
    STORED = "stored"  # only DB
