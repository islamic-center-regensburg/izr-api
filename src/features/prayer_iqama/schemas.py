from __future__ import annotations
from uuid import UUID, uuid4
from datetime import time
from typing import Optional

from sqlalchemy import Column, Time
from sqlmodel import Field, SQLModel

from src.core.db.pagination import PageParams
from src.features.prayer_iqama.enums import IqamaMode, PrayerName


class PrayerIqamaBase(SQLModel):
    mosque_id: UUID = Field(
        ...,
        foreign_key="mosques.id",
        index=True,
    )
    prayer_name: PrayerName = Field(..., description="Name of the prayer")
    mode: IqamaMode = Field(..., description="Iqama mode: fixed or offset")

    # Exactly one of these should be set depending on `mode`
    offset_minutes: Optional[int] = Field(
        default=None,
        description="Offset in minutes from the prayer time if mode is offset",
    )
    fixed_time: Optional[time] = Field(
        default=None,
        sa_column=Column(Time()),
        description="Fixed time for iqama if mode is fixed",
    )


class PrayerIqamaIn(PrayerIqamaBase):
    pass


class PrayerIqamaOut(PrayerIqamaBase):
    id: UUID


class PrayerIqamaTable(PrayerIqamaBase, table=True):
    """
    One row per (mosque_id, prayer_name):
    - mode = fixed  -> fixed_time set, offset_minutes NULL
    - mode = offset -> offset_minutes set, fixed_time NULL
    """

    __tablename__ = "prayer_iqamas"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)


# =========================
# Update
# =========================


class PrayerIqamaUpdate(SQLModel):
    mosque_id: UUID | None = None
    prayer_name: PrayerName | None = None
    mode: IqamaMode | None = None
    offset_minutes: int | None = None
    fixed_time: time | None = None

    # =========================
    # Filter
    # =========================


class PrayerIqamaFilter(PageParams):
    mosque_id: Optional[UUID] = None
    prayer_name: Optional[PrayerName] = None
    mode: Optional[IqamaMode] = None
