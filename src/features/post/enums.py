from enum import StrEnum


class SupportedLanguages(StrEnum):
    AR = "ar"
    DE = "de"
    EN = "en"


class PostContentType(StrEnum):
    EVENT = "event"
    INFO = "info"
    ANNOUNCEMENT = "announcement"


class AllowedMediaType(StrEnum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    WEBP = "image/webp"
    MP4 = "video/mp4"
    PDF = "application/pdf"
