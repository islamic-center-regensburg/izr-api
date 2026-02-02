from datetime import datetime, timezone
from fastapi import File, Form, UploadFile
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional

from src.features.prayer_times_upload.enums import FileTypeEnum


class PrayerTimeUploadIn(BaseModel):
    mosque_id: int = Form(...)
    year: int = Form(...)
    file: UploadFile = File(...)
    file_type: FileTypeEnum = Form(...)


class PrayerTimeUploadBase(SQLModel):
    mosque_id: int = Field(foreign_key="mosques.id", index=True)
    year: int = Field(..., description="Year for which the prayer times are uploaded")
    stored_filename: str = Field(..., description="Stored name of the uploaded file")
    file_type: Optional[FileTypeEnum] = Field(
        None, description="Content type of the uploaded file"
    )


class PrayerTimeUploadCreate(PrayerTimeUploadBase):
    pass


class PrayerTimeUploadTable(PrayerTimeUploadCreate, table=True):
    __tablename__ = "prayer_time_uploads"

    id: int = Field(..., primary_key=True)

    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )


class PrayerTimeUploadOut(PrayerTimeUploadTable):
    pass


class PrayerTimeUploadFilter(SQLModel):
    mosque_id: int | None = None
    year: int | None = None
