import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DUFFEL_ACCESS_TOKEN")

#=====================
# Duffel flight search
#=====================

def search_flights(
    origin,
    destination,
    departure_date,
    return_date=None,
    passenger_count=1,
    cabin_class="economy"
):
    url = "https://api.duffel.com/air/offer_requests"

    headers = {
        "Authorization": f"Bearer {token}",
        "Duffel-Version": "v2",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    slices = [
        {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date
        }
    ]

    if return_date:
        slices.append(
            {
                "origin": destination,
                "destination": origin,
                "departure_date": return_date
            }
        )

    data = {
        "data": {
            "slices": slices,
            "passengers": [
                {"type": "adult"}
                for _ in range(passenger_count)
            ],
            "cabin_class": cabin_class
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