from fastapi import FastAPI
from letsgobro.routers.flights import Flights
from letsgobro.routers.airports import Airports
import uvicorn

app = FastAPI()

app.include_router(Flights, prefix="/v1", tags=['v1'])
app.include_router(Airports, prefix='/v1', tags=['v1'])


if __name__ == '__main__':
    uvicorn.run('app:app',
                host='0.0.0.0',
                port=8080,
                debug=True,
                log_level='debug')
