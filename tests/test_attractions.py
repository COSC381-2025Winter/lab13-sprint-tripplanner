# testing for functions in attractions.py
import os
import sys
from unittest.mock import Mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from unittest.mock import patch
from attractions import AttractionFinder
# Hassan Mouzaihem
# Test 1: Normal working response
@patch("attractions.requests.get")
def test_distance_and_duration_success(mock_get):
    # Arrange
    mock_get.return_value.json.return_value = {
        "status": "OK",
        "rows": [{
            "elements": [{
                "status": "OK",
                "distance": {"text": "3.2 km"},
                "duration": {"text": "7 mins"}
            }]
        }]
    }
   
    # Act
    distance, duration = AttractionFinder.get_distance_and_duration(40.0, -73.0, 40.1, -73.1)
    
    # Assert
    assert distance == "3.2 km"
    assert duration == "7 mins"

# Hassan Mouzaihem
# Test 2: API fails
@patch("attractions.requests.get")
def test_api_status_fail(mock_get):
    # Arrange
    mock_get.return_value.json.return_value = {
        "status": "REQUEST_DENIED"
    }
    
    # Act
    distance, duration = AttractionFinder.get_distance_and_duration(40.0, -73.0, 40.1, -73.1)
    
    # Assert
    assert distance == "N/A"
    assert duration == "N/A"
    
# Hassan Mouzaihem
# Test 3: Location not found
@patch("attractions.requests.get")
def test_element_status_fail(mock_get):
    # Arrange
    mock_get.return_value.json.return_value = {
        "status": "OK",
        "rows": [{
            "elements": [{
                "status": "NOT_FOUND"
            }]
        }]
    }
    
    # Act
    distance, duration = AttractionFinder.get_distance_and_duration(0, 0, 0, 0)
    
    # Assert
    assert distance == "N/A"
    assert duration == "N/A"

# Olivia Daniels
@patch("attractions.requests.get")
def test_successful_get_nearby_attractions(mock_get):
    # Arrange
    longitude = -83.6129
    latitude = 42.2411
    place_type = "restaurant"
    expected_json = {
        "results": [{"name": "Café Aroma"}],
        "status": "OK"
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = lambda: expected_json

    # Act
    finder = AttractionFinder(latitude, longitude)
    response = finder.get_nearby_attractions(place_type)

    # Assert
    assert response["status"] == "OK"
    assert isinstance(response["results"], list)
    assert response["results"][0]["name"] == "Café Aroma"


# Olivia Daniels
@patch("attractions.requests.get")
def test_get_nearby_attractions_with_invalid_API_key(mock_get):
    # Arrange
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = lambda: {"status": "REQUEST_DENIED"}

    # Act
    finder = AttractionFinder(42.2411, -83.6129)
    response = finder.get_nearby_attractions("museum")

    # Assert
    assert "status" in response
    assert response["status"] == "REQUEST_DENIED"

# Olivia Daniels - added for pytest coverage
@patch("attractions.AttractionFinder")
def test_getNearbyAttractions(mock_finder_class):
    mock_finder = Mock()
    mock_finder.get_nearby_attractions.return_value = {"results": []}
    mock_finder_class.return_value = mock_finder

    from attractions import getNearbyAttractions
    result = getNearbyAttractions(-83.61, 42.24, "aquarium")

    assert result == {"results": []}
    mock_finder_class.assert_called_once_with(42.24, -83.61)
    mock_finder.get_nearby_attractions.assert_called_once_with("aquarium")