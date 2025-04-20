# testing for functions in attractions.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from unittest.mock import patch
from attractions import get_distance_and_duration 
# Hassan Mouzaihem
# Test 1: Normal working response
@patch("attractions.requests.get")
def test_distance_and_duration_success(mock_get):
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

    distance, duration = get_distance_and_duration(40.0, -73.0, 40.1, -73.1)
    assert distance == "3.2 km"
    assert duration == "7 mins"

# Hassan Mouzaihem
# Test 2: API fails
@patch("attractions.requests.get")
def test_api_status_fail(mock_get):
    mock_get.return_value.json.return_value = {
        "status": "REQUEST_DENIED"
    }

    distance, duration = get_distance_and_duration(40.0, -73.0, 40.1, -73.1)
    assert distance == "N/A"
    assert duration == "N/A"
    
# Hassan Mouzaihem
# Test 3: Location not found
@patch("attractions.requests.get")
def test_element_status_fail(mock_get):
    mock_get.return_value.json.return_value = {
        "status": "OK",
        "rows": [{
            "elements": [{
                "status": "NOT_FOUND"
            }]
        }]
    }

    distance, duration = get_distance_and_duration(0, 0, 0, 0)
    assert distance == "N/A"
    assert duration == "N/A"
