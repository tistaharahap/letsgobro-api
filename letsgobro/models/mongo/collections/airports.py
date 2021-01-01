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
        for row in result:
            del row['_id']
        return result
