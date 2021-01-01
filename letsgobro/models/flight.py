from pydantic import BaseModel
from letsgobro.models.basic import Coordinate


class FlightSearchRequest(BaseModel):
    coordinate: Coordinate
