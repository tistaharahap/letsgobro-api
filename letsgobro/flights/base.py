import abc


class BaseFlightSearch(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    @abc.abstractmethod
    async def search(origin: str, destination: str, departure_date: str, returning_date: str, adults: int = 1, children: int = 0, infants: int = 0):
        """Search the service for tickets."""
        return
