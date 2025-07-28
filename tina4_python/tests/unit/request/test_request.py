from tina4_python import Request as req


def test_req_001_default_values():
    # REQ-001: Ensure all global variables in the request module have their expected default values.
    assert req.request is None
    assert req.body is None
    assert req.params == {}
    assert req.headers == {}
    assert req.cookies == {}
    assert req.url is None
    assert req.session is None
    assert req.files == {}
    assert req.raw_request is None
    assert req.raw_data is None
    assert req.raw_content is None
    assert req.transport is None
    assert req.asgi_response is None


def test_req_002_mutate_and_reset_request_globals():
    # REQ-002: Test if request globals are mutable and maintain their values correctly
    req.request = "fake_request"
    req.body = {"message": "hello"}
    req.params = {"key": "value"}
    req.headers = {"Authorization": "Bearer token"}
    req.cookies = {"session_id": "abc123"}
    req.url = "/test"
    req.session = {"user_id": 42}
    req.files = {"file": b"binary content"}
    req.raw_request = "raw"
    req.raw_data = b"raw_bytes"
    req.raw_content = b"some_content"
    req.transport = "http"
    req.asgi_response = "response_object"

    assert req.request == "fake_request"
    assert req.body == {"message": "hello"}
    assert req.params["key"] == "value"
    assert req.headers["Authorization"] == "Bearer token"
    assert req.cookies["session_id"] == "abc123"
    assert req.url == "/test"
    assert req.session["user_id"] == 42
    assert req.files["file"] == b"binary content"
    assert req.raw_request == "raw"
    assert req.raw_data == b"raw_bytes"
    assert req.raw_content == b"some_content"
    assert req.transport == "http"
    assert req.asgi_response == "response_object"

    # Reset
    req.request = None
    req.body = None
    req.params = {}
    req.headers = {}
    req.cookies = {}
    req.url = None
    req.session = None
    req.files = {}
    req.raw_request = None
    req.raw_data = None
    req.raw_content = None
    req.transport = None
    req.asgi_response = None


def test_req_003_global_state_is_shared():
    # REQ-003: Simulate state sharing across parts of the app
    req.params["shared"] = "yes"
    assert req.params.get("shared") == "yes"

    req.headers["X-Test"] = "HeaderValue"
    assert "X-Test" in req.headers

    # Clean up
    req.params.clear()
    req.headers.clear()


def test_req_004_type_integrity():
    # REQ-004: Ensure default types remain consistent
    assert isinstance(req.params, dict)
    assert isinstance(req.headers, dict)
    assert isinstance(req.cookies, dict)
    assert isinstance(req.files, dict)
