from typing import Optional

from sqlmodel import Field, SQLModel

from src.data_layer.prayer_time.enums import (
    CalculationMethod,
    CalendarMethod,
    LatitudeAdjustmentMethod,
    MidnightMode,
    School,
    Shafaq,
)


class PrayerTimeConfiguration(SQLModel, table=True):
    __tablename__ = "prayer_times"  # pyright: ignore [reportAssignmentType]

    id: int = Field(default=None, primary_key=True, index=True)

    mosque_id: int = Field(foreign_key="mosques.id", index=True)
    calculation_method: CalculationMethod = Field(
        description="Calculation method for prayer times"
    )
    school: School = Field(
        description="Juristic school for Asr prayer time calculation"
    )
    midnight_mode: MidnightMode = Field(
        description="Midnight mode for Isha calculation"
    )
    latitude_adjustment_method: LatitudeAdjustmentMethod = Field(
        description="Latitude adjustment method for Fajr and Isha calculation"
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
