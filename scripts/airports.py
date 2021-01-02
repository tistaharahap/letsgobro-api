# Initialize and build airport collection
import json
import logging
import os
from os import environ

from functional import seq
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, StringField, connect, disconnect

BASIC_COLLECTION = 'airports/basic.json'
RICH_COLLECTION_PATH = 'airports/collections'

MONGO_USER = environ.get('MONGO_USER')
MONGO_PASSWORD = environ.get('MONGO_PASSWORD')
MONGO_HOST = environ.get('MONGO_HOST')
MONGO_DB = environ.get('MONGO_DB')
MONGO_CONN_STRING = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DB}?retryWrites=true&w=majority'

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s: %(message)s')

logging.debug(f'Mongo Conn String: {MONGO_CONN_STRING}')


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


def load_json(json_path: str):
    with open(json_path, 'r', encoding='utf-8-sig') as f:
        json_obj = json.load(f)

    return json_obj


def main():
    basic_dict = load_json(json_path=BASIC_COLLECTION)
    basic_coll = []
    for k, v in basic_dict.items():
        basic_coll.append(v)

    def _upper(row):
        row['iata'] = row['iata'].upper()
        return row

    basic_coll = seq(basic_coll)\
        .filter(lambda x: x.get('iata') is not None and x.get('iata') != '')\
        .map(_upper)

    def _merge(rich_row):
        basic_row = basic_coll.find(lambda x: x.get('iata') == rich_row.get('id').upper())

        airport = Airport()
        airport.iata = rich_row.get('id').upper()
        airport.name = rich_row.get('name')
        airport.name_english = rich_row.get('nameEnglish')
        airport.city = rich_row.get('city')
        airport.country = rich_row.get('country')
        airport.description = rich_row.get('description')
        airport.location = GeoJson()
        airport.location.type = 'Point'
        airport.location.coordinates = [basic_row.get('lon'), basic_row.get('lat')]

        return airport

    rich_coll = []
    for root, dirs, files in os.walk(RICH_COLLECTION_PATH):
        rich_coll = seq(files)\
            .filter(lambda x: basic_coll.find(lambda y: y.get('iata') == x.replace('.json', '').upper()) is not None)\
            .map(lambda x: os.path.join(root, x))\
            .map(lambda x: load_json(json_path=x))\
            .map(_merge)\
            .to_list()

    logging.debug(f'We have {len(rich_coll)} cleaned airports')

    logging.debug('Connecting to MongoDB')
    connect(host=MONGO_CONN_STRING)

    logging.debug('Going to bulk insert to MongoDB')
    Airport.objects.insert(rich_coll)

    logging.debug('Disconnecting from MongoDB')
    disconnect()


if __name__ == '__main__':
    main()
