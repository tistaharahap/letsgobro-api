from typing import Optional, List
from pydantic import BaseModel
from letsgobro.models.basic import Distance


class FlightSearchRequest(BaseModel):
    origin: str
    outbound_date: str
    inbound_date: str
    budget: int
    adults: int = 1
    children: Optional[int] = 0
    infants: Optional[int] = 0


class Airport(BaseModel):
    iata: str
    name: str
    name_english: Optional[str] = None
    city: str
    country: str
    description: str
    latitude: float
    longitude: float
    distance: Optional[Distance] = None


class Destination(BaseModel):
    airport: Airport
    origin: str
    destination: str
    link: str


class FlightSearchResponse(BaseModel):
    budget: int
    outbound_date: str
    inbound_date: str
    adults: int
    children: int
    infants: int
    destinations: List[Destination] = []

