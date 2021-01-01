from fastapi import APIRouter

from letsgobro.models.mongo import connect_to_mongodb, disconnect_mongodb
from letsgobro.models.mongo.collections.airports import Airport

Airports = APIRouter()


@Airports.get('/airports')
async def airports(latitude: float, longitude: float, max_distance_in_km: int = 50):
    await connect_to_mongodb()

    query = [
        {
            '$geoNear': {
                'near': {
                    'type': 'Point',
                    'coordinates': [longitude, latitude],
                },
                'distanceField': 'distance.in_meters',
                'maxDistance': max_distance_in_km * 1000,
                'spherical': True
            }
        }
    ]
    nearest_airports = await Airport.aggregate(query=query)

    await disconnect_mongodb()

    return {
        'airports': nearest_airports
    }
