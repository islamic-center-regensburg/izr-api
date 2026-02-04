from enum import StrEnum


class IqamaMode(StrEnum):
    FIXED = "fixed"
    OFFSET = "offset"


class PrayerName(StrEnum):
    FAJR = "fajr"
    DHUHR = "dhuhr"
    ASR = "asr"
    MAGHRIB = "maghrib"
    ISHA = "isha"
    JUMAH = "jumah"
