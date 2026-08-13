import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DUFFEL_ACCESS_TOKEN")


def search_flights(origin, destination, departure_date):
    url = "https://api.duffel.com/air/offer_requests"

    headers = {
        "Authorization": f"Bearer {token}",
        "Duffel-Version": "v2",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "data": {
            "slices": [
                {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date
                }
            ],
            "passengers": [
                {
                    "type": "adult"
                }
            ],
            "cabin_class": "economy"
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    if response.status_code != 201:
        print("Flight search failed.")
        print(response.text)
        return []

    result = response.json()
    offers = result["data"]["offers"]

    return offers