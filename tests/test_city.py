#testing for functions in city.py

import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from city import getLongAndLat

# Oliver McMillen
def test_empty_cityst_entered(capsys):
    
    # Arrange
    input_value = ""

    # Act
    response = getLongAndLat(input_value)

    # Assert
    captured = capsys.readouterr()
    assert "status" in response
    assert response["status"] in ["ZERO_RESULTS", "INVALID_REQUEST", "ERROR"]

#Oliver McMillen
def test_numerical_cityst_entered(capsys):
    
    # Arrange
    input_value = "999"

    # Act
    response = getLongAndLat(input_value)

    # Assert
    assert "status" in response
    assert response["status"] in ["ZERO_RESULTS", "INVALID_REQUEST", "ERROR"]

