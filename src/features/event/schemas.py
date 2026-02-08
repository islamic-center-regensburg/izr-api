from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import File, Form, UploadFile
from pydantic import BaseModel
from sqlmodel import SQLModel, Field

from src.core.db.pagination import PageParams, PaginatedResponse
from src.features.event.enums import SupportedLanguages


class EventBase(SQLModel):
    mosque_id: int = Field(
        ..., description="ID of the mosque associated with the event"
    )


class EventCreate(EventBase):
    valid_to: datetime | None = Field(
        None,
        description="Validity date of the event. If not provided, it will be set to 30 days from the creation date.",
    )


class EventTable(EventBase, table=True):
    __tablename__ = "events"

    id: int = Field(..., primary_key=True)
    created_at: datetime = Field(
        ...,
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation date of the event",
    )
    updated_at: datetime = Field(
        ...,
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last update date of the event",
    )
    valid_to: datetime = Field(
        ...,
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30),
        description="Validity date of the event",
    )


class EventRead(EventTable):
    pass


class EventFilter(BaseModel):
    date_from: Optional[datetime] = None
    language: SupportedLanguages | None = None


class EventPaginationFilter(EventFilter, PageParams):
    pass


class EventTranslationBase(SQLModel):
    title: str | None = Field(None, description="Title of the event")
    description: str | None = Field(None, description="Description of the event")
    language: SupportedLanguages = Field(
        ..., description="Language of the event translation"
    )
    media: str | None = Field(
        None, description="Object key that points to S3 Object Directory"
    )


class EventTranslationRead(EventTranslationBase):
    pass


class EventTranslationIn(SQLModel):
    title: str | None = Form(None, description="Title of the event")
    language: SupportedLanguages = Form(
        ..., description="Language of the event translation"
    )
    media: list[UploadFile] | None = File(
        None, description="List of media files associated with the event translation"
    )


class EventTranslationTable(EventTranslationBase, table=True):
    __tablename__ = "event_translations"

    id: int = Field(..., primary_key=True)
    event_id: int = Field(
        ..., foreign_key="events.id", description="ID of the associated event"
    )


class EventOut(SQLModel):
    id: int
    mosque_id: int
    created_at: datetime
    updated_at: datetime
    valid_to: datetime
    translations: list[EventTranslationRead]


EventListOut = PaginatedResponse[EventOut]
