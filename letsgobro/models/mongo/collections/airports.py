from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentField, ListField


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
