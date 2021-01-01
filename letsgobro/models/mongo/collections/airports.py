from mongoengine import Document, StringField, GeoPointField


class Airport(Document):
    iata = StringField(required=True)
    location = GeoPointField(required=True)
    name = StringField(required=True)
    name_english = StringField(required=True)
    city = StringField(required=True)
    country = StringField(required=True)
    description = StringField()
