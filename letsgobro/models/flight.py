from typing import Optional
from pydantic import BaseModel
from letsgobro.models.basic import Coordinate, Distance


class FlightSearchRequest(BaseModel):
    coordinate: Coordinate


class Airport(BaseModel):
    iata: str
    name: str
    city: str
    country: str
    description: str
    latitude: float
    longitude: float
    distance: Optional[Distance] = None

