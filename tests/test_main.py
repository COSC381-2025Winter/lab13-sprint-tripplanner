# testing for functions/main in main.py
import os
import sys
from io import StringIO
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

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