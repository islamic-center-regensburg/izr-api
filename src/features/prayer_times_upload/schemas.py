from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class PrayerTimeUploadTable(SQLModel, table=True):
    __tablename__ = "prayer_time_uploads"

    id: Optional[int] = Field(default=None, primary_key=True)
    mosque_id: int = Field(foreign_key="mosques.id", index=True)

    original_filename: str = Field(
        ..., description="Original name of the uploaded file"
    )
    stored_filename: str = Field(..., description="Stored name of the uploaded file")
    content_type: Optional[str] = Field(
        None, description="Content type of the uploaded file"
    )
    year: int = Field(..., description="Year for which the prayer times are uploaded")

    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(datetime.timezone.utc), index=True
    )

    rows_inserted: int = 0
    status: str = "success"
    error: Optional[str] = None
