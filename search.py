from amadeus import Client, ResponseError
import os

amadeus = Client(
    client_id=os.getenv("AMADEUS_CLIENT_ID"),
    client_secret=os.getenv("AMADEUS_CLIENT_SECRET")
)

def search_flights(origin, dest, date, max_price):
    try:
        res = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=dest,
            departureDate=date,
            adults=1,
            max=3
        )
        matches = []
        for offer in res.data:
            eur = float(offer['price']['total'])
            krw = eur * 1400
            if krw <= max_price:
                matches.append(f"{origin}→{dest} {date} | 약 {int(krw)}원")
        return matches
    except ResponseError as e:
        print(e)
        return []
