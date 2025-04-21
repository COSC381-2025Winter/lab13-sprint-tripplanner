import requests
import os
from dotenv import load_dotenv

class City:
    def __init__(self, name):
        self.name = name
        self.latitude = None
        self.longitude = None

    def get_coordinates(self):
        load_dotenv()
        API_KEY = os.getenv("GEOCODING_API_KEY")

        geocodeURL = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": self.name,
            "key": API_KEY,
        }

        response = requests.get(geocodeURL, params=params)
        data = response.json()

        if "results" in data and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            self.latitude = location["lat"]
            self.longitude = location["lng"]
            return self.latitude, self.longitude
        else:
            raise ValueError("No coordinates found for the given city.")