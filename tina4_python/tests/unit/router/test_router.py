import pytest
from tina4_python.Router import Router
import tina4_python
from unittest.mock import MagicMock

def test_get_variables_extracts_correct_params():
    url = "/user/123"
    route_path = "/user/{id}"
    expected = {"id": "123"}
    result = Router.get_variables(url, route_path)
    assert result == expected

def test_match_returns_true_for_matching_route():
    url = "/product/456"
    route = "/product/{productId}"
    assert Router.match(url, route) is True
    assert Router.variables == {"productId": "456"}

def test_match_returns_false_for_non_matching_route():
    url = "/user/123/profile"
    route = "/user/{id}"
    assert Router.match(url, route) is False

def test_clean_url_removes_double_slashes():
    url = "/user//profile"
    cleaned = Router.clean_url(url)
    assert cleaned == "/user/profile"

def test_add_route_creates_route_entry():
    tina4_python.tina4_routes = {}
    callback = lambda x: x
    Router.add("GET", "/test/path", callback)
    assert callback in tina4_python.tina4_routes
    route_info = tina4_python.tina4_routes[callback]
    assert route_info["route"] == "/test/path"
    assert route_info["method"] == "GET"

def test_add_route_with_parameters_parses_params():
    tina4_python.tina4_routes = {}
    callback = lambda x: x
    Router.add("GET", "/item/{itemId}/details", callback)
    assert "params" in tina4_python.tina4_routes[callback]
    assert tina4_python.tina4_routes[callback]["params"] == ["itemId"]
