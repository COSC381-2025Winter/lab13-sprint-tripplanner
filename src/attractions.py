import requests
import os
from dotenv import load_dotenv

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

class AttractionFinder:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def get_nearby_attractions(self, place_type):
        radius = 1000
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{self.latitude},{self.longitude}",
            "radius": radius,
            "type": place_type,
            "key": self.api_key,
        }

        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def get_distance_and_duration(origin_lat, origin_lng, destination_lat, destination_lng):
        load_dotenv()
        api_key = os.getenv("DISTANCE_MATRIX_API_KEY")

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": f"{origin_lat},{origin_lng}",
            "destinations": f"{destination_lat},{destination_lng}",
            "key": api_key,
            "mode": "Driving",
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") == "OK":
            element = data["rows"][0]["elements"][0]
            if element["status"] == "OK":
                return element["distance"]["text"], element["duration"]["text"]
        return "N/A", "N/A"

def getNearbyAttractions(longitude, latitude, place_type):
    return AttractionFinder(latitude, longitude).get_nearby_attractions(place_type)
