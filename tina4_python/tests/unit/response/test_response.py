import types
import json
import pytest

from tina4_python.Response import Response
import tina4_python.Response as response_module
from tina4_python import Constant


@pytest.fixture(autouse=True)
def reset_globals():
    # Reset the global variables before each test
    response_module.headers = {}
    response_module.content = ""
    response_module.http_code = Constant.HTTP_OK
    response_module.content_type = Constant.TEXT_HTML
    yield


def test_response_with_string():
    res = Response("Hello World")
    assert res.content == "Hello World"
    assert res.content_type == Constant.TEXT_HTML
    assert res.http_code == Constant.HTTP_OK


def test_response_with_dict():
    data = {"name": "Tina4", "version": 1}
    res = Response(data)
    assert res.content_type == Constant.APPLICATION_JSON
    parsed = json.loads(res.content)
    assert parsed["name"] == "Tina4"
    assert parsed["version"] == 1


def test_response_with_list():
    res = Response(["apple", "banana"])
    assert res.content_type == Constant.APPLICATION_JSON
    assert json.loads(res.content) == ["apple", "banana"]


def test_response_with_bool_true():
    res = Response(True)
    assert res.content == "True"
    assert res.content_type == Constant.TEXT_HTML


def test_response_with_bool_false():
    res = Response(False)
    assert res.content == "False"
    assert res.content_type == Constant.TEXT_HTML


def test_response_with_module_type():
    mod = types
    res = Response(mod)
    assert res.content_type == Constant.APPLICATION_JSON
    assert "error" in json.loads(res.content)


def test_response_with_custom_http_code_and_headers():
    custom_headers = {"X-Test": "123"}
    res = Response("Success", http_code_in=201, headers_in=custom_headers)
    assert res.http_code == 201
    assert res.headers["X-Test"] == "123"


def test_response_redirect_sets_correct_headers():
    res = Response.redirect("/home")
    assert res.http_code == Constant.HTTP_REDIRECT
    assert res.headers["Location"] == "/home"
    assert res.content == ""
    assert res.content_type == Constant.TEXT_HTML


def test_add_header_updates_global_headers():
    Response.add_header("X-Custom", "value")
    res = Response("Test")
    assert res.headers["X-Custom"] == "value"
