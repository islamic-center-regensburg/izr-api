from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4
from fastapi import File, Form, UploadFile
from pydantic import BaseModel
from sqlmodel import SQLModel, Field

from src.core.db.pagination import PageParams, PaginatedResponse
from src.features.media.schemas import MediaOut
from src.features.post.enums import PostContentType, SupportedLanguages


class PostBase(SQLModel):
    mosque_id: UUID = Field(
        ..., description="ID of the mosque associated with the post"
    )
    content_type: PostContentType = Field(..., description="Type of post content")


class PostCreate(PostBase):
    valid_to: datetime | None = Field(
        None,
        description="Validity date of the post. If not provided, it will be set to 30 days from the creation date.",
    )


class PostTable(PostBase, table=True):
    __tablename__ = "posts"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(
        ...,
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation date of the post",
    )
    updated_at: datetime = Field(
        ...,
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last update date of the post",
    )
    valid_to: datetime = Field(
        ...,
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30),
        description="Validity date of the post",
    )


class PostRead(PostTable):
    pass


class PostFilter(BaseModel):
    date_from: Optional[datetime] = None
    language: SupportedLanguages | None = None
    content_type: PostContentType | None = None


class PostPaginationFilter(PostFilter, PageParams):
    pass


class PostTranslationBase(SQLModel):
    title: str | None = Field(None, description="Title of the post")
    description: str | None = Field(None, description="Description of the post")
    language: SupportedLanguages = Field(
        ..., description="Language of the post translation"
    )


class PostTranslationOut(PostTranslationBase):
    media: list[MediaOut] | None = Field(
        None, description="Media Urls with Object keys"
    )
    pass


class PostTranslationIn(SQLModel):
    title: str | None = Form(None, description="Title of the post")
    language: SupportedLanguages = Form(
        ..., description="Language of the post translation"
    )
    media: list[UploadFile] | None = File(
        None, description="List of media files associated with the post translation"
    )


class PostTranslationTable(PostTranslationBase, table=True):
    __tablename__ = "post_translations"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    post_id: UUID = Field(
        ..., foreign_key="posts.id", description="ID of the associated post"
    )
    media: str | None = Field(
        None, description="Object key that points to S3 Object Directory"
    )


class PostTranslationRead(PostTranslationTable):
    pass


class PostOut(SQLModel):
    id: UUID
    mosque_id: UUID
    content_type: PostContentType
    created_at: datetime
    updated_at: datetime
    valid_to: datetime
    translations: list[PostTranslationOut]


PostListOut = PaginatedResponse[PostOut]
