import requests
import os
from dotenv import load_dotenv



def getLongAndLat(location):

    #Loading environment variables to get the API key
    load_dotenv()
    API_KEY = os.getenv("GEOCODING_API_KEY")

    geocodeURL = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": API_KEY,
    }

    response = requests.get(geocodeURL, params=params)
    data = response.json()
    return data

def getNearbyAttractions(longitude, latitude, place_type):
    #Set a radius of 1000 meters, this can be changed if we want
    radius = 1000

    #Loading environment variables to get the API key
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{longitude},{latitude}",
        "radius": radius,
        "type": place_type,
        "key": API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data

def get_distance_and_duration(origin_lat, origin_lng, destination_lat, destination_lng):
    """Calculate distance and duration between origin and destination."""

    API_KEY = os.getenv("DISTANCE_MATRIX_API_KEY")

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": f"{origin_lat},{origin_lng}",
        "destinations": f"{destination_lat},{destination_lng}",
        "key": API_KEY,
        "mode": "Driving",
    }
    response = requests.get(url, params=params)
    data = response.json()


    if data.get("status") == "OK":
        element = data["rows"][0]["elements"][0]
        if element["status"] == "OK":
            return element["distance"]["text"], element["duration"]["text"]
    return "N/A", "N/A"

def show_available_place_types():
    """Display available place types"""
    print("Available Place Types")
    print("---------------------")
    print("1.Aquarium")
    print("2.Art Gallery")
    print("3.Bakery")
    print("4.Bar")
    print("5.Museum")
    print("6.Restaurant")
    print("7.Tourist Attraction")
    print("8.Zoo")
    print("---------------------")

def show_menu():
    """Display the menu options."""
    print("\nTrip Planner")
    print("Enter q at any point to Exit")

def main():
    keepRunning = True
    lat = -1
    lng = -1

    show_menu()

    while(keepRunning):
        # request user input as City, ST
        location = input("\nEnter City, ST: ")
        if location.upper() == "Q":
            print("Goodbye!")
            break

        # start extraction of Long and Lat from location specified
        response = getLongAndLat(location)
        if response.get("status") == "OK":
            location_data = response["results"][0]["geometry"]["location"]
            lat = location_data["lat"]
            lng = location_data["lng"]
        else:
            print("Could not retrieve coordinates. Error:", response.get("error_message", "Try again"))
            continue

        # get place type input from user
        show_available_place_types()
        choice = input("\nSelect a place type: ")
        match choice:
            case "1":
                place = "aquarium"
            case "2":
                place = "art_gallery"
            case "3": 
                place = "bakery"
            case "4":
                place = "bar"
            case "5":
                place = "museum"
            case "6":
                place = "restaurant"
            case "7":
                place = "tourist_attraction"
            case "8":
                place = "zoo"
            case "q"|"Q":
                print("Goodbye!")
                break
            case _:
                print("Invalid place type, please try again.")
                continue
    
        #Get and display nearby results
        result = getNearbyAttractions(lat, lng, place)

        print(f"\nNearby {place.capitalize()}s:\n")

        for place in result.get("results", []):
            name = place.get("name", "Unknown Place")
            dest = place.get("geometry", {}).get("location", {})
            dest_lat = dest.get("lat")
            dest_lng = dest.get("lng")

            if dest_lat is not None and dest_lng is not None:
                distance, duration = get_distance_and_duration(lat, lng, dest_lat, dest_lng)
                print(f"{name} — {distance} away, approx. {duration}")
            else:
                print(f"{name} — Location unavailable")

        
if __name__ == "__main__":
    main()