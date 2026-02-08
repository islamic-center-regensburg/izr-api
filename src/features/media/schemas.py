from __future__ import annotations


from fastapi import Query
from pydantic import BaseModel
from sqlmodel import Field

from src.integrations.minio.enums import DirectoryEnum


class MediaOut(BaseModel):
    object: str = Field(..., description="The filename or object key of the media file")
    url: str = Field(..., description="Presigned URL to access the media file")


class DirectoryQuery(BaseModel):
    mosque_id: int = Query(..., description="The ID of the mosque")
    dir: str = Field(..., description="The directory path containing media files")
    media_category: DirectoryEnum = Field(
        ..., description="The category of media files (e.g., events, prayer_times)"
    )
