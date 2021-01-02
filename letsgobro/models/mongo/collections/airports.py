from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentField, ListField
from typing import List


class GeoJson(EmbeddedDocument):
    type = StringField(required=True,
                       default='Point')
    coordinates = ListField(required=True,
                            max_length=2)


class Airport(Document):
    iata = StringField(required=True)
    location = EmbeddedDocumentField(GeoJson,
                                     required=True)
    name = StringField(required=True)
    name_english = StringField(required=True)
    city = StringField(required=True)
    country = StringField(required=True)
    description = StringField()

    @staticmethod
    async def aggregate(query: List):
        result = list(Airport._get_collection().aggregate(query))
        return result

    @staticmethod
    async def reverse_geocode_using_iata(iata: str):
        query = [
            {
                '$match': {
                    'iata': iata
                }
            },
            {
                '$project': {
                    'latitude': {
                        '$arrayElemAt': ['$location.coordinates', 1]
                    },
                    'longitude': {
                        '$arrayElemAt': ['$location.coordinates', 0]
                    },
                }
            }
        ]
        result = await Airport.aggregate(query=query)
        if len(result) == 0:
            return []

        return result[0]

    @staticmethod
    async def find_destinations(origin: str, max_distance_in_km: int = 1000, min_distance_in_km: int = 120):
        coordinates = await Airport.reverse_geocode_using_iata(iata=origin)
        result = await Airport.find_nearest_airport(latitude=coordinates.get('latitude'),
                                                    longitude=coordinates.get('longitude'),
                                                    max_distance_in_km=max_distance_in_km,
                                                    min_distance_in_km=min_distance_in_km)

        return result

    @staticmethod
    async def find_nearest_airport(latitude: float, longitude: float, max_distance_in_km: int, min_distance_in_km: int = 0):
        query = [
            {
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': [longitude, latitude],
                    },
                    'distanceField': 'distance.in_meters',
                    'maxDistance': max_distance_in_km * 1000,
                    'minDistance': min_distance_in_km * 1000,
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

        return await Airport.aggregate(query=query)
