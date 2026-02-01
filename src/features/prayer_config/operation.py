from src.core.db.pagination import PaginationBuilder
from src.features.prayer_config.exceptions import PrayerConfigNotFoundException
from src.features.prayer_config.schemas import (
    PrayerConfigurationFilter,
    PrayerConfigurationIn,
    PrayerTimeConfigurationUpdate,
)
from src.core.db.database_repository_provider import DatabaseRepositoryProvider
from src.core.db.filters import Filter, Operator
from src.features.prayer_config.schemas import PrayerConfigurationTable


class PrayerConfigOperation:
    def __init__(self, db_repository_provider: DatabaseRepositoryProvider):
        self.db_repository = db_repository_provider

    def get_all_prayer_configurations(self, filter: PrayerConfigurationFilter):
        filters = [
            Filter(attribute="mosque_id", operator=Operator.EQ, value=filter.mosque_id),
            Filter(attribute="id", operator=Operator.EQ, value=filter.id),
        ]
        with self.db_repository.get_database_repository() as db:
            configs = db.get_all(PrayerConfigurationTable, filters=filters)
            total = db.count(PrayerConfigurationTable, filters=filters)
            return PaginationBuilder.build(
                items=configs,
                total=total,
                page=filter.page,
                size=filter.size,
            )

    def get_by_id(self, prayer_config_id: int):
        with self.db_repository.get_database_repository() as db:
            config = db.get_by_id(PrayerConfigurationTable, prayer_config_id)
            return config

    def add_prayer_configuration(
        self, mosque_id: str, config_data: PrayerConfigurationIn
    ):
        with self.db_repository.get_database_repository() as db:
            prayer_config = PrayerConfigurationTable(
                mosque_id=int(mosque_id),
                calculation_method=config_data.calculation_method,
                school=config_data.school,
                midnight_mode=config_data.midnight_mode,
                latitude_adjustment_method=config_data.latitude_adjustment_method,
                tune=config_data.tune,
                imsak_tune=config_data.imsak_tune,
                fajr_tune=config_data.fajr_tune,
                sunrise_tune=config_data.sunrise_tune,
                dhuhr_tune=config_data.dhuhr_tune,
                asr_tune=config_data.asr_tune,
                maghrib_tune=config_data.maghrib_tune,
                isha_tune=config_data.isha_tune,
                midnight_tune=config_data.midnight_tune,
                fajr_angle=config_data.fajr_angle,
                maghrib_angle=config_data.maghrib_angle,
                isha_angle=config_data.isha_angle,
                shafaq=config_data.shafaq,
                calendar_method=config_data.calendar_method,
            )
            db.create(prayer_config)
            return prayer_config

    def update_prayer_configuration(
        self, prayer_config_id: str, config_data: PrayerTimeConfigurationUpdate
    ):
        with self.db_repository.get_database_repository() as db:
            filters = [
                Filter(
                    field_name="id",
                    operator=Operator.EQUAL,
                    value=int(prayer_config_id),
                )
            ]
            prayer_config = db.get_all(PrayerConfigurationTable, filters=filters)
            if not prayer_config:
                raise PrayerConfigNotFoundException(
                    f"No prayer configuration found with ID: {prayer_config_id}"
                )
            prayer_config = prayer_config[0]
            for key, value in config_data.model_dump(exclude_unset=True).items():
                setattr(prayer_config, key, value)
            db.update(prayer_config)
            return prayer_config
