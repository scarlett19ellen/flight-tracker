from duffel_api import search_flights
import math
import csv
print("This is TravelFest")
airports = {}
with open("airports.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            code = row["iata_code"]

            if code:
                airports[code] = {
                    "name": row["name"],
                    "lat": float(row["latitude_deg"]),
                    "lon": float(row["longitude_deg"])
                }

def calculate_distance(lat1, lon1, lat2, lon2):
        radius = 3958.8

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return radius * c
while True:
    departure = input("Enter departure airport: ").upper()
    arrival = input("Enter arrival airport: ").upper()

    if len(departure) != 3 or not departure.isalpha():
        print("Invalid departure airport code.")
    elif len(arrival) != 3 or not arrival.isalpha():
        print("Invalid arrival airport code. ")
    elif departure not in airports: 
        print("Departure airport not found.")
    elif arrival not in airports:
        print("Arrival airport not found.")
    else:
        print()
        print("Your flight route: ")
        print(departure, "-", airports[departure]["name"])
        print("->")
        print(arrival, "-", airports[arrival]["name"])
        distance = calculate_distance(
        airports[departure]["lat"],
        airports[departure]["lon"],
        airports[arrival]["lat"],
        airports[arrival]["lon"],
        )
    print("Distance:", round(distance), "miles"),
    departure_date = input("Enter departure date (YYYY-MM-DD): ")
    offers = search_flights(
            departure,
            arrival,
            departure_date
            )
        
    if offers:
        cheapest_offers = sorted(
        offers,
        key=lambda offer: float(offer["total_amount"])
        )[:5]

        print()
        print("Top 5 cheapest flights:")

        for number, offer in enumerate(cheapest_offers, start=1):
            print(
                number,
                "-",
                offer["owner"]["name"],
                "-",
                offer["total_currency"],
                offer["total_amount"]
    )
    
    average_speed = 500
    flight_time = distance / average_speed
    hours = int(flight_time)
    minutes = round((flight_time - hours) * 60)

    print("Estimated flight time:", hours, "hours", minutes, "minutes")
    print("Distance:", round(distance), "miles")

    again = input("Would you like to search another flight? (yes/no): ").lower()
    if again != "yes":
        print("Thanks for using TravelFest")
        break