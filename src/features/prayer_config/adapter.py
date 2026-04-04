from __future__ import annotations

from typing import Any, Dict


from src.features.prayer_config.schemas import PrayerConfiguration
from src.features.prayer_times.models.schemas import AlAdhanQueryParams


class PrayerConfigurationAdapter:
    @staticmethod
    def to_al_adhan_query_params(
        cfg: PrayerConfiguration | None,
    ) -> AlAdhanQueryParams:
        if cfg is None:
            return AlAdhanQueryParams()

        q: Dict[str, Any] = {
            "method": int(cfg.calculation_method),
            "school": int(cfg.school),
            "midnightMode": int(cfg.midnight_mode),
            "latitudeAdjustmentMethod": int(cfg.latitude_adjustment_method),
            "adjustment": int(cfg.adjustment),
            "shafaq": str(cfg.shafaq),
        }

        if cfg.fajr_angle is not None:
            q["fajr"] = float(cfg.fajr_angle)
        if cfg.maghrib_angle is not None:
            q["maghrib"] = float(cfg.maghrib_angle)
        if cfg.isha_angle is not None:
            q["isha"] = float(cfg.isha_angle)
        if cfg.calendar_method:
            q["calendarMethod"] = str(cfg.calendar_method)
        if cfg.tune:
            tune_values = [
                int(cfg.imsak_tune or 0),
                int(cfg.fajr_tune or 0),
                int(cfg.sunrise_tune or 0),
                int(cfg.dhuhr_tune or 0),
                int(cfg.asr_tune or 0),
                int(cfg.maghrib_tune or 0),
                int(cfg.isha_tune or 0),
                int(cfg.midnight_tune or 0),
            ]
            q["tune"] = ",".join(map(str, tune_values))

        return AlAdhanQueryParams.model_validate(q)
