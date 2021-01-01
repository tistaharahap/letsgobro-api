from fastapi import FastAPI
from letsgobro.routers.flights import Flights
import uvicorn

app = FastAPI()

app.include_router(Flights, prefix="/v1", tags=['v1'])


if __name__ == '__main__':
    uvicorn.run('app:app',
                host='0.0.0.0',
                port=8000,
                debug=True,
                log_level='debug')
