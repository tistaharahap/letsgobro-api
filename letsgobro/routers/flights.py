from fastapi import APIRouter
from letsgobro.models.flight import FlightSearchRequest, FlightSearchResponse
from letsgobro.models.mongo.collections.airports import Airport
from letsgobro.flights.forwarder.traveloka import forward
from letsgobro.models.mongo import connect_to_mongodb, disconnect_mongodb
from letsgobro.flights.helper import get_distances_from_budget

Flights = APIRouter()


@Flights.post('/flights', response_model=FlightSearchResponse)
async def flights(request: FlightSearchRequest):
    await connect_to_mongodb()

    min_distance_in_km, max_distance_in_km = get_distances_from_budget(budget=request.budget)
    destinations = await Airport.find_destinations(origin=request.origin,
                                                   min_distance_in_km=min_distance_in_km,
                                                   max_distance_in_km=max_distance_in_km)

    def _build_destination(origin: str, destination: dict, departure_date: str, returning_date: str, adults: int,
                           children: int, infants: int):
        forward_link = forward(origin=origin,
                               destination=destination.get('iata'),
                               departure_date=departure_date,
                               returning_date=returning_date,
                               adults=adults,
                               children=children,
                               infants=infants)
        return {
            'airport': destination,
            'origin': origin,
            'destination': destination.get('iata'),
            'link': forward_link
        }

    destinations = [_build_destination(origin=request.origin,
                                       destination=row,
                                       departure_date=request.outbound_date,
                                       returning_date=request.inbound_date,
                                       adults=request.adults,
                                       children=request.children,
                                       infants=request.infants) for row in destinations]

    await disconnect_mongodb()

    return {
        'budget': request.budget,
        'outbound_date': request.outbound_date,
        'inbound_date': request.inbound_date,
        'adults': request.adults,
        'children': request.children,
        'infants': request.infants,
        'destinations': destinations
    }
