from fastapi import APIRouter

from letsgobro.models.mongo import connect_to_mongodb, disconnect_mongodb
from letsgobro.models.mongo.collections.airports import Airport

Airports = APIRouter()


@Airports.get('/airports')
async def airports(latitude: float, longitude: float, max_distance_in_km: int = 50):
    await connect_to_mongodb()

    nearest_airports = list(Airport._get_collection().find({
        'location': {
            '$nearSphere': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [longitude, latitude]
                },
                '$maxDistance': max_distance_in_km * 1000
            }
        }
    }))
    for row in nearest_airports:
        del row['_id']

    await disconnect_mongodb()

    return {
        'airports': nearest_airports
    }