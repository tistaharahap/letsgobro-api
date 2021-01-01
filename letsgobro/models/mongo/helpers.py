from mongoengine import connect, disconnect
from os import environ


MONGO_USER = environ.get('MONGO_USER')
MONGO_PASSWORD = environ.get('MONGO_PASSWORD')
MONGO_HOST = environ.get('MONGO_HOST')
MONGO_DB = environ.get('MONGO_DB')
MONGO_CONN_STRING = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DB}?retryWrites=true&w=majority'


async def connect_to_mongodb():
    connect(host=MONGO_CONN_STRING)


async def disconnect_mongodb():
    disconnect()
