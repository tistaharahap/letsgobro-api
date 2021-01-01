from pydantic import BaseModel
from typing import List


class Coordinate(BaseModel):
    latitude: float
    longitude: float


class GeoJson(BaseModel):
    type: str
    coordinates: List


class Distance(BaseModel):
    in_meters: float
