from duffel_api import search_flights
from datetime import datetime, date
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

# =====================
# Helper Functions 
#======================

def calculate_distance(lat1, lon1, lat2, lon2):
    # Calculate the distance between two airports in miles.
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
        
def format_duration(duration):
    # Function to return correct hour format
    duration = duration.replace("PT", "")

    hours = 0
    minutes = 0

    if "H" in duration:
        hours_part, duration = duration.split("H")
        hours = int(hours_part)

    if "M" in duration:
        minutes = int(duration.replace("M", ""))

    return f"{hours}h {minutes}m"

def get_valid_date(prompt, after_date=None):
    # Only valid dates be inserted as input
    while True:
        date_text = input(prompt)

        try:
            entered_date = datetime.strptime(
                date_text,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            print("Please use YYYY-MM-DD.")
            continue

        if entered_date <= date.today():
            print("Date must be in the future.")
            continue

        if after_date and entered_date <= after_date:
            print("Return date must be after departure date.")
            continue

        return date_text, entered_date

#=====================
# Main Flight Search
#=====================

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
        trip_type = input(
            "One-way or round trip? (one-way/round): "
            ).lower()
        departure_date, departure_date_obj = get_valid_date(
            "Enter departure date (YYYY-MM-DD): "
            )
        return_date = None

    

        if trip_type == "round":
            return_date, return_date_obj = get_valid_date(
                "Enter return date (YYYY-MM-DD): ",
                departure_date_obj
            )

        while True:
            try:
                passenger_count = int(input("How many passengers? "))

                if passenger_count >= 1:
                    break

                print("Please enter at least 1 passenger.")

            except ValueError:
                print("Please enter a number.")

        valid_cabins = [
            "economy",
            "premium_economy",
            "business",
            "first"
        ]

        while True:
            cabin_class = input(
                "Cabin class (economy/premium_economy/business/first): "
            ).lower()

            if cabin_class in valid_cabins:
                break

            print("Please enter a valid cabin class.")

        offers = search_flights(
            departure,
            arrival,
            departure_date,
            return_date,
            passenger_count,
            cabin_class
        )
        
                
        if offers:
            cheapest_offers = sorted(
            offers,
            key=lambda offer: float(offer["total_amount"])
            )[:5]

            print()
            print("Top 5 cheapest flights:")

            for number, offer in enumerate(cheapest_offers, start=1):
                print()

                print(f"{number}. {offer['owner']['name']}")
                print(
                    f"Total price: {offer['total_currency']} "
                    f"{offer['total_amount']}"
                )

                for slice_number, flight_slice in enumerate(offer["slices"]):
                    segments = flight_slice["segments"]
                    first_segment = segments[0]
                    last_segment = segments[-1]
                    departure_time = first_segment["departing_at"].split("T")[1][:5]
                    arrival_time = last_segment["arriving_at"].split("T")[1][:5]
                    connections = len(segments) - 1

                    if connections == 0:
                        stops = "Nonstop"
                    elif connections == 1:
                        stops = "1 stop"
                    else:
                        stops = f"{connections} stops"

                    duration = format_duration(flight_slice["duration"])

                    if slice_number == 0:
                        direction = "Outbound"
                    else:
                        direction = "Return"

                    print()
                    print(direction)
                    print(
                        first_segment["origin"]["iata_code"],
                        "→",
                        last_segment["destination"]["iata_code"]
                    )
                    print("Departure:", departure_time)
                    print("Arrival:", arrival_time)
                    print("Stops:", stops)
                    print("Duration:", duration)
        
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