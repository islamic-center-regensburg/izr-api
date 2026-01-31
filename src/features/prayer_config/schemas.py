from typing import Optional

from sqlmodel import Field, SQLModel

from src.core.db.pagination import PageParams
from src.features.prayer_config.enums import (
    CalculationMethod,
    CalendarMethod,
    LatitudeAdjustmentMethod,
    MidnightMode,
    School,
    Shafaq,
)


class PrayerConfigurationBase(SQLModel):
    mosque_id: int = Field(foreign_key="mosques.id", index=True)

    calculation_method: CalculationMethod = Field(
        description="Calculation method for prayer times"
    )
    school: School = Field(
        description="Juristic school for Asr prayer time calculation",
        default=School.SHAFI,
    )
    midnight_mode: MidnightMode = Field(
        default=MidnightMode.STANDARD, description="Midnight mode for Isha calculation"
    )
    latitude_adjustment_method: LatitudeAdjustmentMethod = Field(
        default=LatitudeAdjustmentMethod.ANGLE_BASED,
        description="Latitude adjustment method for Fajr and Isha calculation",
    )
    tune: bool = Field(
        default=False, description="Whether the prayer times are manually tuned"
    )
    imsak_tune: Optional[int] = Field(
        default=0, description="Minutes to adjust Imsak time"
    )
    fajr_tune: Optional[int] = Field(
        default=0, description="Minutes to adjust Fajr time"
    )
    sunrise_tune: Optional[int] = Field(
        default=0, description="Minutes to adjust Sunrise time"
    )
    dhuhr_tune: Optional[int] = Field(
        default=0, description="Minutes to adjust Dhuhr time"
    )
    asr_tune: Optional[int] = Field(default=0, description="Minutes to adjust Asr time")
    maghrib_tune: Optional[int] = Field(
        default=0, description="Minutes to adjust Maghrib time"
    )
    isha_tune: Optional[int] = Field(
        default=0, description="Minutes to adjust Isha time"
    )
    midnight_tune: Optional[int] = Field(
        default=0, description="Minutes to adjust Midnight time"
    )
    fajr_angle: Optional[float] = Field(
        default=None, description="Angle for Fajr calculation (if applicable)"
    )
    maghrib_angle: Optional[float] = Field(
        default=None, description="Angle for Maghrib calculation (if applicable)"
    )
    isha_angle: Optional[float] = Field(
        default=None, description="Angle for Isha calculation (if applicable)"
    )
    shafaq: Shafaq = Field(
        default=Shafaq.GENERAL,
        description="Type of twilight for Isha calculation (if applicable)",
    )
    calendar_method: CalendarMethod = Field(
        default=CalendarMethod.HJCoSA,
        description="Method for Islamic calendar calculation",
    )

    adjustment: int = Field(
        default=0, le=2, ge=-2, description="Days to adjust the Hijri date"
    )


class PrayerConfigurationTable(PrayerConfigurationBase, table=True):
    __tablename__ = "prayer_configurations"  # pyright: ignore [reportAssignmentType]
    id: int = Field(default=None, primary_key=True, index=True)


class PrayerTimeConfigurationIn(PrayerConfigurationBase):
    pass


class PrayerTimeConfigurationOut(PrayerTimeConfigurationIn):
    id: int
    mosque_id: int


class PrayerTimeConfigurationUpdate(SQLModel):
    mosque_id: Optional[int] | None = None
    calculation_method: Optional[CalculationMethod] | None = None
    school: Optional[School] | None = None
    midnight_mode: Optional[MidnightMode] | None = None
    latitude_adjustment_method: Optional[LatitudeAdjustmentMethod] | None = None
    tune: Optional[bool] | None = None
    imsak_tune: Optional[int] | None = None
    fajr_tune: Optional[int] | None = None
    sunrise_tune: Optional[int] | None = None
    dhuhr_tune: Optional[int] | None = None
    asr_tune: Optional[int] | None = None
    maghrib_tune: Optional[int] | None = None
    isha_tune: Optional[int] | None = None
    midnight_tune: Optional[int] | None = None
    fajr_angle: Optional[float] | None = None
    maghrib_angle: Optional[float] | None = None
    isha_angle: Optional[float] | None = None
    shafaq: Optional[Shafaq] | None = None
    calendar_method: Optional[CalendarMethod] | None = None


class PrayerConfigurationFilter(PageParams):
    id: Optional[int] = None
    mosque_id: Optional[int] = None
