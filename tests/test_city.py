#testing for functions in city.py

import os
import sys
import pytest
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/tripplanner")))
from tripplanner.city import City

# Oliver McMillen
def test_empty_cityst_entered():

    # Arrange
    input_value = ""

    # Act
    city = City(input_value)
    
    # Assert
    with pytest.raises(ValueError):
        city.get_coordinates()

#Oliver McMillen
def test_numerical_cityst_entered():

    # Arrange
    input_value = "999"

    # Act
    city = City(input_value)

    # Assert
    with pytest.raises(ValueError):
        city.get_coordinates()

#Oliver McMillen
@patch("tripplanner.city.requests.get")
def test_validCity_entered(mock_get):
    # Arrange: fake response from API
    mock_get.return_value.json.return_value = {
        "results": [{
            "geometry": {
                "location": {
                    "lat": 42.2411,
                    "lng": -83.612993
                }
            }
        }],
        "status": "OK"
    }

    city = City("Ypsilanti, MI")

    # Act
    lat, lng = city.get_coordinates()

    # Assert
    assert isinstance(lat, float)
    assert isinstance(lng, float)