# LetsGoBro

Use this to go to a random destination within a budget. Optimized for South East Asia travelling. Written to learn FastAPI, was impressed.

MongoDB is used for geospatial queries.

## Running

```shell
$ git clone git@github.com:tistaharahap/letsgobro-api.git
$ cd letsgobro-api
$ virtualenv env
$ . env/bin/activate
$ pip install -r requirements.txt
$ MONGO_USER=user MONGO_PASSWORD=password MONGO_HOST=host MONGO_DB=db python scripts/airports.py # seed mongodb, only needed once
$ MONGO_USER=user MONGO_PASSWORD=password MONGO_HOST=host MONGO_DB=db python app.py
```

### Endpoints

Since this is a FastAPI implementation, just run the API and go to `http://localhost:8000/docs`.

## Env Vars

| Name | Description |
| :--- | :--- |
| `MONGO_USER` | User for MongoDB |
| `MONGO_PASSWORD` | Password for MongoDB |
| `MONGO_HOST` | Host for MongoDB |
| `MONGO_DB` | Database for MongoDB |

