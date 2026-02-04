from src.core.db.pagination import PaginatedResponse
from src.features.prayer_iqama.operation import PrayerIqamaOperation
from src.features.prayer_iqama.schemas import (
    PrayerIqamaFilter,
    PrayerIqamaIn,
    PrayerIqamaOut,
    PrayerIqamaUpdate,
)


class PrayerIqamaComponent:
    def __init__(
        self,
        prayer_iqama_operation: PrayerIqamaOperation,
    ):
        self.__prayer_iqama_operation = prayer_iqama_operation

    def get_prayer_iqamas(
        self,
        filter: PrayerIqamaFilter,
    ) -> PaginatedResponse[PrayerIqamaOut]:
        return self.__prayer_iqama_operation.get_all_prayer_iqamas(filter)

    def get_prayer_iqamas_for_mosque(
        self,
        mosque_id: int,
    ) -> list[PrayerIqamaOut]:
        return self.__prayer_iqama_operation.get_all_prayer_iqamas_for_mosque(mosque_id)

    def create_prayer_iqama(
        self,
        prayer_iqama_in: PrayerIqamaIn,
    ) -> PrayerIqamaOut:
        return self.__prayer_iqama_operation.create(prayer_iqama_in)

    def update_prayer_iqama(
        self,
        prayer_iqama_id: int,
        prayer_iqama_update: PrayerIqamaUpdate,
    ) -> PrayerIqamaOut:
        return self.__prayer_iqama_operation.update(
            prayer_iqama_id, prayer_iqama_update
        )
