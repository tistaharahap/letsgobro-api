from letsgobro.flights.base import BaseFlightSearch
from bs4 import BeautifulSoup
import cfscrape


scraper = cfscrape.create_scraper()


class TiketDotCom(BaseFlightSearch):

    @staticmethod
    async def search_bulk(origin: str, destinations: list, departure_date: str, returning_date: str, adults: int = 1, children: int = 0, infants: int = 0):
        result = []
        for row in destinations:
            result.append(await TiketDotCom.search(origin=origin,
                                                   destination=row,
                                                   departure_date=departure_date,
                                                   returning_date=returning_date,
                                                   adults=adults,
                                                   children=children,
                                                   infants=infants))
        return result

    @staticmethod
    async def search(origin: str, destination: str, departure_date: str, returning_date: str, adults: int = 1, children: int = 0, infants: int = 0):
        url = 'http://www.tiket.com/pesawat/cari?d=%s&a=%s&date=%s&ret_date=%s&adult=%s&child=%s&infant=%s'
        url = url % (origin, destination, departure_date, returning_date, adults, children, infants)
        headers = {
            'Referer': 'http://en.tiket.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5'
        }

        response = scraper.get(url, headers=headers)
        body = response.text
        if not 'summary_pricetotal' in body:
            print('No price')
            return None

        tree = BeautifulSoup(body, 'lxml')

        price = tree.find(id='summary_pricetotal').get('rel')
        if not price or int(price) == 0:
            print('Invalid price')
            return None

        try:
            outbound_airline = tree.find(id='summary_depart').find('td', {'class': 't3'}).small.string.split()
            outbound_airline = ' '.join(outbound_airline)
            inbound_airline = tree.find(id='summary_return').find('td', {'class': 't3'}).small.string.split()
            inbound_airline = ' '.join(inbound_airline)
        except AttributeError:
            print('No airlines')
            return None

        return {
            'outbound_airline': outbound_airline,
            'inbound_airline': inbound_airline,
            'price': price
        }
