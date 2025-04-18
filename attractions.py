import requests
import os
from dotenv import load_dotenv

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