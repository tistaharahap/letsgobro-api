from fastapi import APIRouter
from typing import List

from letsgobro.models.mongo import connect_to_mongodb, disconnect_mongodb
from letsgobro.models.mongo.collections.airports import Airport
from letsgobro.models.flight import Airport as AirportResponse

Airports = APIRouter()


@Airports.get('/airports', response_model=List[AirportResponse])
async def airports(latitude: float, longitude: float, max_distance_in_km: int = 50):
    await connect_to_mongodb()

    nearest_airports = await Airport.find_nearest_airport(latitude=latitude,
                                                          longitude=longitude,
                                                          max_distance_in_km=max_distance_in_km)

    await disconnect_mongodb()

    return nearest_airports
