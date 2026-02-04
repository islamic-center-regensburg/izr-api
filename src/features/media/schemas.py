from __future__ import annotations

from typing import Optional

from fastapi import Form, UploadFile
from sqlmodel import SQLModel, Field

from src.core.db.pagination import PageParams
from src.features.media.enums import MediaFileType


class MediaBase(SQLModel):
    mosque_id: int = Field(
        ..., description="ID of the mosque associated with the media"
    )
    object_key: str = Field(..., description="Object key of the media file in storage")
    type: MediaFileType = Field(..., description="Media file to upload")  # noqa: F821


class MediaCreate(MediaBase):
    pass


class MediaIn(SQLModel):
    file: UploadFile = Form(..., description="Media file to upload")
    type: MediaFileType = Form(..., description="Media file to upload")  # noqa: F821
    mosque_id: int = Form(
        ...,
        description="ID of the mosque associated with the media",
    )


class MediaTable(MediaBase, table=True):
    __tablename__ = "media"
    id: int | None = Field(default=None, primary_key=True, index=True)


class MediaOut(MediaTable):
    url: str = Field(..., description="Presigned URL to access the media file")
    pass


class MediaFilter(PageParams):
    id: Optional[int] = None
    mosque_id: Optional[int] = None
