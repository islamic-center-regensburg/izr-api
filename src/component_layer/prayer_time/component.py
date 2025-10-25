from src.data_layer.mosque.operation import MosqueOperation
from src.data_layer.prayer_time.operation import PrayerTimeOperation
from aladhan import Coordinates, Client


class PrayerTimeComponent:
    def __init__(
        self,
        prayer_time_operation: PrayerTimeOperation,
        mosque_operation: MosqueOperation,
    ):
        self.prayer_time_operation = prayer_time_operation
        self.mosque_operation = mosque_operation

    def get_today_prayer_times_for_mosque(self, mosque_id: str):
        mosque = self.mosque_operation.get_mosque_by_id(mosque_id)
        if not mosque:
            raise ValueError(f"No mosque found with ID: {mosque_id}")

        config = self.prayer_time_operation.get_prayer_time_configuration_by_mosque(
            mosque_id
        )
        if not config:
            raise ValueError(
                f"No prayer time configuration found for mosque ID: {mosque_id}"
            )

        coordinates = Coordinates(latitude=mosque.latitude, longitude=mosque.longitude)
        client = Client(coordinates)
        prayer_times = client.get_today_times()
        return prayer_times
