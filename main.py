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
    # result = getNearbyAttractions("42.24193221947446", "-83.62000302245067", "museum")
    # for place in result.get("results", []):
    #     print(place["name"])
    show_menu()

    # request user input as City, ST
    location = input("Enter City, ST: ")
    place = input("Enter place type: ")
    print(getLongAndLat(location))
    
if __name__ == "__main__":
    main()
    