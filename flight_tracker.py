import math
print("This is TravelFest")

while True:
    departure = input("Enter departure airport: ").upper()
    arrival = input("Enter arrival airport: ").upper()
    airports = {
        "JFK": {
            "name": "John F. Kennedy International Airport",
            "lat": 40.6413,
            "lon": -73.7781
        },
        "LAX": {
            "name": "Los Angeles International Airport",
            "lat": 33.9416,
            "lon": -118.4085
        },
        "EWR": {
            "name": "Newark Liberty International Airport",
            "lat": 40.6895,
            "lon": -74.1745
        },
        "GRU": {
            "name": "São Paulo/Guarulhos International Airport",
            "lat": -23.4356,
            "lon": -46.4731
        },
        "GIG": {
            "name": "Rio de Janeiro/Galeão International Airport",
            "lat": -22.8090,
            "lon": -43.2506
        }
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
        print("→")
        print(arrival, "-", airports[arrival]["name"])
        distance = calculate_distance(
        airports[departure]["lat"],
        airports[departure]["lon"],
        airports[arrival]["lat"],
        airports[arrival]["lon"]
    )
    
    average_speed = 500
    flight_time = distance / average_speed
    hours = int(flight_time)
    minutes = round((flight_time - hours) * 60)

    print("Estimated flight time:", hours, "hours", minutes, "minutes")
    print("Distance:", round(distance), "miles")

    again = input("Would you like to search another flight? (yes/no): ").lower()
    if again != "yes":
        print("Thanks for using FlightFest")
        break