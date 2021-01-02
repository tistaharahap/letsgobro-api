from datetime import datetime


def forward(origin: str, destination: str, departure_date: str, returning_date: str, adults: int = 1, children: int = 0, infants: int = 0):
    now = datetime.utcnow()
    year = str(now.year)

    if departure_date.startswith(year):
        departure_date = departure_date.split('-')
        departure_date = f'{departure_date[2]}-{departure_date[1]}-{departure_date[0]}'
    if returning_date.startswith(year):
        returning_date = returning_date.split('-')
        returning_date = f'{returning_date[2]}-{returning_date[1]}-{returning_date[0]}'

    url = f'https://www.traveloka.com/en-id/flight/fulltwosearch?ap={origin}.{destination}&dt={departure_date}.{returning_date}&ps={adults}.{children}.{infants}&sc=ECONOMY'
    return url
