import pytest
import tina4_python
from tina4_python.Swagger import Swagger, description, summary, secure, tags, example, params
from tina4_python import Constant


@pytest.fixture(autouse=True)
def clear_routes():
    tina4_python.tina4_routes.clear()
    yield
    tina4_python.tina4_routes.clear()


def dummy_callback():
    pass


def test_add_methods_store_values():
    Swagger.add_descripton("desc", dummy_callback)
    Swagger.add_summary("sum", dummy_callback)
    Swagger.add_secure(dummy_callback)
    Swagger.add_tags(["tag1"], dummy_callback)
    Swagger.add_example({"foo": "bar"}, dummy_callback)
    Swagger.add_params(["id=123"], dummy_callback)

    stored = tina4_python.tina4_routes[dummy_callback]["swagger"]
    assert stored["description"] == "desc"
    assert stored["summary"] == "sum"
    assert stored["secure"] is True
    assert stored["tags"] == ["tag1"]
    assert stored["example"] == {"foo": "bar"}
    assert stored["params"] == ["id=123"]


@pytest.mark.parametrize(
    "path,expected",
    [
        ("/items/{id}", [{"name": "id", "in": "path", "type": "string"}]),
        ("/no/params", []),
    ]
)
def test_get_path_inputs(path, expected):
    assert Swagger.get_path_inputs(path) == expected


def test_get_swagger_entry_with_example():
    entry = Swagger.get_swagger_entry(
        url="/items/{id}",
        method=Constant.TINA4_POST,
        tags=["t1"],
        summary="sum",
        description="desc",
        produces=["application/json"],
        security=True,
        params=["q=test"],
        example={"foo": "bar"},
        responses={"200": {"desc": "ok"}}
    )
    assert entry["tags"] == ["t1"]
    assert entry["summary"] == "sum"
    assert entry["description"] == "desc"
    assert any(p["in"] in ("query", "path") for p in entry["parameters"])
    assert entry["security"] == [{"bearerAuth": []}]
    assert "requestBody" in entry  # POST + example should keep requestBody


def test_get_swagger_entry_without_example_removes_requestbody():
    entry = Swagger.get_swagger_entry(
        url="/items",
        method=Constant.TINA4_GET,
        tags=[],
        summary="",
        description="",
        produces=[],
        security=False,
        params=[],
        example=None,
        responses={}
    )
    assert "requestBody" not in entry


def test_parse_swagger_fills_defaults():
    raw = {}
    parsed = Swagger.parse_swagger(raw)
    assert parsed["tags"] == []
    assert parsed["params"] == []
    assert parsed["description"] == ""
    assert parsed["summary"] == ""
    assert parsed["example"] is None
    assert parsed["secure"] is None


def test_parse_swagger_converts_tags_to_list():
    parsed = Swagger.parse_swagger({"tags": "single"})
    assert parsed["tags"] == ["single"]


def test_get_json_builds_correct_output():
    # Prepare tina4_python.tina4_routes with minimal route
    tina4_python.tina4_routes["cb"] = {
        "route": "/items/{id}",
        "method": Constant.TINA4_GET,
        "swagger": {
            "tags": ["t1"],
            "summary": "sum",
            "description": "desc",
            "example": None,
            "secure": False,
            "params": ["x=1"]
        }
    }

    class DummyRequest:
        headers = {"host": "testserver"}

    result = Swagger.get_json(DummyRequest())
    assert result["openapi"] == "3.0.0"
    assert result["host"] == "testserver"
    assert "/items/{id}" in result["paths"]
    assert "get" in result["paths"]["/items/{id}"]


def test_decorator_functions_update_swagger():
    @description("desc")
    @summary("sum")
    @secure()
    @tags(["tag"])
    @example({"foo": "bar"})
    @params(["q=1"])
    def my_route():
        pass

    stored = tina4_python.tina4_routes[my_route]["swagger"]
    assert stored["description"] == "desc"
    assert stored["summary"] == "sum"
    assert stored["secure"] is True
    assert stored["tags"] == ["tag"]
    assert stored["example"] == {"foo": "bar"}
    assert stored["params"] == ["q=1"]


def test_invalid_parameter_format_handled():
    @params(["invalid"])  # Missing '=' in param string
    def bad_route():
        pass

    stored = tina4_python.tina4_routes[bad_route]["swagger"]
    # Still stores as provided, but will likely not parse correctly in Swagger entry
    assert stored["params"] == ["invalid"]

    # Build swagger entry and ensure it doesn't crash
    entry = Swagger.get_swagger_entry(
        url="/test",
        method=Constant.TINA4_GET,
        tags=[],
        summary="",
        description="",
        produces=[],
        security=False,
        params=stored["params"],
        example=None,
        responses={}
    )
    assert "parameters" in entry  # Even with invalid param format, it should include an empty parameters list

def test_missing_host_header_defaults():
    tina4_python.tina4_routes["cb"] = {
        "route": "/items",
        "method": Constant.TINA4_GET,
        "swagger": {
            "tags": [],
            "summary": "",
            "description": "",
            "example": None,
            "secure": False,
            "params": []
        }
    }

    class DummyRequest:
        headers = {}  # No 'host' key

    result = Swagger.get_json(DummyRequest())
    assert result["host"] != ""  # Should have some default value
    assert "/items" in result["paths"]
