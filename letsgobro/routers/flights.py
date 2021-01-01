from fastapi import APIRouter
from letsgobro.models.flight import FlightSearchRequest


Flights = APIRouter()


@Flights.post('/flights')
async def flights(request: FlightSearchRequest):
    return {
        'coordinate': request.coordinate.dict()
    }
