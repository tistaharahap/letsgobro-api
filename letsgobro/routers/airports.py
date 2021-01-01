from fastapi import APIRouter
from typing import List

from letsgobro.models.mongo import connect_to_mongodb, disconnect_mongodb
from letsgobro.models.mongo.collections.airports import Airport
from letsgobro.models.flight import Airport as AirportResponse

Airports = APIRouter()


@Airports.get('/airports', response_model=List[AirportResponse])
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
        },
        {
            '$project': {
                '_id': 0
            }
        },
        {
            '$project': {
                'iata': '$iata',
                'latitude': {
                    '$arrayElemAt': ['$location.coordinates', 1]
                },
                'longitude': {
                    '$arrayElemAt': ['$location.coordinates', 0]
                },
                'name': '$name',
                'name_english': '$name_english',
                'city': '$city',
                'country': '$country',
                'description': '$description',
                'distance': '$distance'
            }
        }
    ]
    nearest_airports = await Airport.aggregate(query=query)
    print(nearest_airports)

    await disconnect_mongodb()

    return nearest_airports
