#testing for functions in city.py

import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from city import City

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
def test_validCity_entered():
    # Arrange
    input_value = "Ypsilanti, MI"

    # Act
    city = City(input_value)
    lat, lng = city.get_coordinates()


    # Assert
    assert isinstance(lat, float)
    assert "42.2" in str(lat)

    assert isinstance(lng, float)
    assert "-83.6" in str(lng)
