from enum import StrEnum


class MediaFileType(StrEnum):
    IMAGE = "image"
    VIDEO = "video"


class AllowedMeidaType(StrEnum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    WEBP = "image/webp"
    MP4 = "video/mp4"
