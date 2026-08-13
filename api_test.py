import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DUFFEL_ACCESS_TOKEN")

origin = input("Enter departure airport: ").upper()
destination = input("Enter arrival airport: ").upper()
departure_date = input("Enter departure date (YYYY-MM-DD): ")

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

print("Status:", response.status_code)

if response.status_code == 201:
    result = response.json()

    offers = result["data"]["offers"]

    print("Offers found:", len(offers))

    if offers:
        cheapest = min(
            offers,
            key=lambda offer: float(offer["total_amount"])
        )

        print(
            "Cheapest price:",
            cheapest["total_currency"],
            cheapest["total_amount"]
        )

        print(
            "Airline:",
            cheapest["owner"]["name"]
        )

else:
    print(response.text)