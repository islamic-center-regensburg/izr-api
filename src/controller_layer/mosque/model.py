from pydantic import BaseModel


class MosqueIn(BaseModel):
    name: str
    address: str
    latitude: str
    longitude: str
    city: str
    country: str
    timezone: str
