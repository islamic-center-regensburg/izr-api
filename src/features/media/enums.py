from enum import StrEnum


class MediaFileType(StrEnum):
    IMAGE = "image"
    VIDEO = "video"


class AllowedMediaType(StrEnum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    WEBP = "image/webp"
    MP4 = "video/mp4"
