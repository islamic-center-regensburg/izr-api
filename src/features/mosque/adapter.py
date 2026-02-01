from typing import Any
from src.features.mosque.schemas import Mosque


class MosqueQueryAdapter:
    @staticmethod
    def to_query(mosque: Mosque | None) -> dict[str, Any]:
        if mosque is None:
            return {}
        return {
            "latitude": mosque.latitude,
            "longitude": mosque.longitude,
            "timezone": mosque.timezone,
        }
