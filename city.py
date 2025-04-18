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