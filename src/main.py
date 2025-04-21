import city
import attractions

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

        try:
            user_city = city.City(location)
            lat, lng = user_city.get_coordinates()
        except ValueError as e:
            print("Could not retrieve coordinates. Error:", str(e))
            continue

        # get place type input from user
        attractions.show_available_place_types()
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
    
        finder = attractions.AttractionFinder(lat, lng)
        result = finder.get_nearby_attractions(place)

        print(f"\nNearby {place.capitalize()}s:\n")

        for place in result.get("results", []):
            name = place.get("name", "Unknown Place")
            dest = place.get("geometry", {}).get("location", {})
            dest_lat = dest.get("lat")
            dest_lng = dest.get("lng")

            if dest_lat is not None and dest_lng is not None:
                distance, duration = attractions.AttractionFinder.get_distance_and_duration(lat, lng, dest_lat, dest_lng)
                print(f"{name} — {distance} away, approx. {duration}")
            else:
                print(f"{name} — Location unavailable")

        
if __name__ == "__main__":
    main()