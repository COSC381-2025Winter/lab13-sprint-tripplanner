import requests
import os
from dotenv import load_dotenv

# Load environment variables once at the top
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")  # Use the same key for all API requests

def get_long_and_lat(location):
    """Get latitude and longitude from a location string using Geocoding API."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": API_KEY,
    }
    response = requests.get(url, params=params)
    return response.json()

def get_nearby_attractions(latitude, longitude, place_type, radius=1000):
    """Find nearby places of the given type."""
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{latitude},{longitude}",
        "radius": radius,
        "type": place_type,
        "key": API_KEY,
    }
    response = requests.get(url, params=params)
    return response.json()

def get_distance_and_duration(origin_lat, origin_lng, destination_lat, destination_lng):
    """Calculate distance and duration between origin and destination."""
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": f"{origin_lat},{origin_lng}",
        "destinations": f"{destination_lat},{destination_lng}",
        "key": API_KEY,
        "mode": "walking",
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") == "OK":
        element = data["rows"][0]["elements"][0]
        if element["status"] == "OK":
            return element["distance"]["text"], element["duration"]["text"]
    return "N/A", "N/A"

def show_menu():
    """Display the menu options."""
    print("\nTrip Planner")
    print("Available Place Types")
    print("1. Aquarium")
    print("2. Art Gallery")
    print("3. Bakery")
    print("4. Bar")
    print("5. Museum")
    print("6. Restaurant")
    print("7. Tourist Attraction")
    print("8. Zoo")
    print("Enter q to Exit\n")

def main():
    show_menu()

    while True:
        location_input = input("Enter City, ST: ").strip()
        if location_input.lower() == 'q':
            return

        place_type = input("Enter place type: ").strip().lower()
        geo_data = get_long_and_lat(location_input)

        if geo_data.get("status") == "OK":
            coords = geo_data["results"][0]["geometry"]["location"]
            lat, lng = coords["lat"], coords["lng"]
            print(f"\nCoordinates Found: Latitude {lat}, Longitude {lng}")
            break
        else:
            print("Could not retrieve coordinates. Error:", geo_data.get("error_message", "Try again."))

    # Get and display nearby results
    result = get_nearby_attractions(lat, lng, place_type)

    print(f"\nNearby {place_type.capitalize()}s:\n")

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
