#testing for functions in city.py

import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from city import getLongAndLat

# Oliver McMillen
def test_empty_cityst_entered():
    
    # Arrange
    input_value = ""

    # Act
    response = getLongAndLat(input_value)

    # Assert
    assert "status" in response
    assert response["status"] in ["ZERO_RESULTS", "INVALID_REQUEST", "ERROR"]


#Oliver McMillen
def test_numerical_cityst_entered():
    
    # Arrange
    input_value = "999"

    # Act
    response = getLongAndLat(input_value)

    # Assert
    assert "status" in response
    assert response["status"] in ["ZERO_RESULTS", "INVALID_REQUEST", "ERROR"]


#Oliver McMillen
def test_validCity_entered():

    # Arrange
    input_value = "Ypsilanti, MI"

    # Act
    response = getLongAndLat(input_value)

    # Assert
    assert "status" in response
    assert response["status"] == "OK"
    location = response["results"][0]["geometry"]["location"]

    assert isinstance(location["lat"], float)
    assert "42.2411" in str(location["lat"])
    
    assert isinstance(location["lng"], float)
    assert "83.6129" in str(location["lng"])
