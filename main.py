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
    location = input("Enter Location: ")
    place = input("Enter place type: ")
    

if __name__ == "__main__":
    main()
    