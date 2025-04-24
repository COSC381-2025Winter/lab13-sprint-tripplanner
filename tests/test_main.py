# testing for functions/main in main.py
import os
import sys
from io import StringIO
import pytest
from unittest.mock import MagicMock, patch, Mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/tripplanner")))

from main import show_menu, main
from attractions import show_available_place_types


@pytest.fixture
def mock_city(monkeypatch):
    mock_city_class = MagicMock()
    mock_city_instance = MagicMock()
    mock_city_instance.get_coordinates.side_effect = ValueError("Invalid city name")
    mock_city_class.return_value = mock_city_instance
    monkeypatch.setitem(__import__("main").__dict__, "city", MagicMock(City=mock_city_class))
    return mock_city_class

@pytest.fixture
def mock_attractions(monkeypatch):
    mock = MagicMock()
    monkeypatch.setitem(__import__("main").__dict__, "attractions", mock)
    return mock

# Angelia Philip
def test_show_menu_output(capsys):
    show_menu()
    captured = capsys.readouterr()
    assert "Trip Planner" in captured.out
    assert "Enter q at any point to Exit" in captured.out

# Angelia Philip
def test_show_available_place_types_output(capsys):
    show_available_place_types()
    captured = capsys.readouterr()
    assert "Available Place Types" in captured.out
    assert "1.Aquarium" in captured.out
    assert "8.Zoo" in captured.out

# Angelia Philip
def test_main_invalid_city(monkeypatch, capsys, mock_city):
    monkeypatch.setattr('sys.stdin', StringIO("InvalidCityXYZ\nq\n"))

    main()
    captured = capsys.readouterr().out
    assert "Could not retrieve coordinates" in captured
    assert "Goodbye!" in captured
    
# Angelia Philip
def test_main_user_quits_immediately(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO("q\n"))
    main()
    captured = capsys.readouterr().out
    assert "Goodbye!" in captured
#Anglia Philip - added for pytest coverage
@patch("city.City")
@patch("attractions.AttractionFinder.get_distance_and_duration")
def test_main_valid_city_and_place(mock_distance, mock_city_class, monkeypatch, capsys):
    mock_city = Mock()
    mock_city.get_coordinates.return_value = (42.24, -83.61)
    mock_city_class.return_value = mock_city

    def mock_init(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def mock_get_nearby(self, place_type):
        return {
            "results": [{
                "name": "Aquarium",
                "geometry": {"location": {"lat": 42.25, "lng": -83.60}}
            }]
        }

    monkeypatch.setattr("attractions.AttractionFinder.__init__", mock_init)
    monkeypatch.setattr("attractions.AttractionFinder.get_nearby_attractions", mock_get_nearby)

    mock_distance.return_value = ("1.2 km", "5 mins")
    monkeypatch.setattr("sys.stdin", StringIO("Ypsilanti, MI\n1\nq\n"))

    main()
    output = capsys.readouterr().out

    assert "Nearby Aquariums" in output
    assert "Aquarium" in output
    assert "1.2 km" in output
    assert "5 mins" in output
    assert "Goodbye!" in output

#Angelia Philip - added for pytest coverage
@patch("city.City")
def test_main_invalid_place_type(mock_city_class, monkeypatch, capsys):
    mock_city = Mock()
    mock_city.get_coordinates.return_value = (42.24, -83.61)
    mock_city_class.return_value = mock_city

    monkeypatch.setattr("sys.stdin", StringIO("Ypsilanti, MI\n99\nq\n"))

    main()
    output = capsys.readouterr().out

    assert "Invalid place type" in output
    assert "Goodbye!" in output

#Angelia Philip - added for pytest coverage
@patch("city.City")
def test_quit_at_place_type_prompt(mock_city_class, monkeypatch, capsys):
    mock_city = Mock()
    mock_city.get_coordinates.return_value = (42.24, -83.61)
    mock_city_class.return_value = mock_city

    monkeypatch.setattr("sys.stdin", StringIO("Ypsilanti, MI\nq\n"))

    main()
    output = capsys.readouterr().out

    assert "Goodbye!" in output


@pytest.mark.parametrize("choice,place", [
    ("2", "art_gallery"),
    ("3", "bakery"),
    ("4", "bar"),
    ("5", "museum"),
    ("6", "restaurant"),
    ("7", "tourist_attraction"),
    ("8", "zoo"),
])

#Angelia Philip - added for pytest coverage
@patch("city.City")
@patch("attractions.AttractionFinder.get_distance_and_duration")
def test_main_all_place_types(mock_distance, mock_city_class, choice, place, monkeypatch, capsys):
    mock_city = Mock()
    mock_city.get_coordinates.return_value = (42.24, -83.61)
    mock_city_class.return_value = mock_city

    def mock_init(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def mock_get_nearby(self, place_type):
        return {
            "results": [{
                "name": place.title(),
                "geometry": {"location": {"lat": 42.25, "lng": -83.60}}
            }]
        }

    monkeypatch.setattr("attractions.AttractionFinder.__init__", mock_init)
    monkeypatch.setattr("attractions.AttractionFinder.get_nearby_attractions", mock_get_nearby)

    mock_distance.return_value = ("2.0 km", "10 mins")
    monkeypatch.setattr("sys.stdin", StringIO(f"Ypsilanti, MI\n{choice}\nq\n"))

    main()
    output = capsys.readouterr().out
    assert f"Nearby {place.replace('_', ' ').capitalize()}s" in output
    assert "2.0 km" in output
    assert "10 mins" in output

#Angelia Philip - added for pytest coverage
@patch("city.City")
def test_main_missing_destination_coords(mock_city_class, monkeypatch, capsys):
    mock_city = Mock()
    mock_city.get_coordinates.return_value = (42.24, -83.61)
    mock_city_class.return_value = mock_city

    def mock_init(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def mock_get_nearby(self, place_type):
        return {
            "results": [{
                "name": "Unknown Place",
                "geometry": {"location": {}}
            }]
        }

    monkeypatch.setattr("attractions.AttractionFinder.__init__", mock_init)
    monkeypatch.setattr("attractions.AttractionFinder.get_nearby_attractions", mock_get_nearby)

    monkeypatch.setattr("sys.stdin", StringIO("Ypsilanti, MI\n1\nq\n"))

    main()
    output = capsys.readouterr().out
    assert "Unknown Place — Location unavailable" in output
