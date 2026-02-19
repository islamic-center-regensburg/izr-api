from enum import StrEnum


class SupportedLanguages(StrEnum):
    AR = "ar"
    DE = "de"
    EN = "en"


class PostContentType(StrEnum):
    EVENT = "event"
    INFO = "info"
    ANNOUNCEMENT = "announcement"
