import asyncio
import base64
import json
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock

import pytest
import tina4_python
from tina4_python.Webserver import Webserver, is_int
from tina4_python import Constant
import pytest
pytestmark = pytest.mark.asyncio



@pytest.mark.asyncio
async def test_is_int():
    assert is_int("5") is True
    assert is_int("abc") is False


@pytest.mark.asyncio
async def test_get_content_length():
    ws = Webserver("localhost", 8000)
    ws.lowercase_headers = {"content-length": "10"}
    assert await ws.get_content_length() == 10
    ws.lowercase_headers = {}
    assert await ws.get_content_length() == 0


@pytest.mark.asyncio
async def test_get_content_body_urlencoded():
    ws = Webserver("localhost", 8000)
    ws.lowercase_headers = {"content-type": "application/x-www-form-urlencoded"}
    ws.content_raw = b"a=1&b=two"
    out = await ws.get_content_body(10)
    assert out == {"a": "1", "b": "two"}


@pytest.mark.asyncio
async def test_get_content_body_json_and_plain():
    ws = Webserver("localhost", 8000)
    ws.lowercase_headers = {"content-type": "application/json"}
    data = {"a": 1}
    ws.content_raw = json.dumps(data).encode()
    out = await ws.get_content_body(len(ws.content_raw))
    assert out == data

    ws.lowercase_headers = {"content-type": "application/json"}
    ws.content_raw = b"not json"
    out = await ws.get_content_body(len(ws.content_raw))
    assert out == "not json"

    ws.lowercase_headers = {"content-type": "text/plain"}
    ws.content_raw = b"hello"
    out = await ws.get_content_body(5)
    assert out == "hello"


@pytest.mark.asyncio
async def test_get_content_body_default_base64():
    ws = Webserver("localhost", 8000)
    ws.lowercase_headers = {}
    ws.content_raw = b"rawbytes"
    out = await ws.get_content_body(9)
    assert "data" in out
    assert base64.b64decode(out["data"]) == b"rawbytes"


@pytest.mark.asyncio
async def test_send_header_and_basic_headers():
    ws = Webserver("localhost", 8000)
    headers = []
    ws.send_header("X-Test", "1", headers)
    assert "X-Test: 1" in headers

    headers = []
    await ws.send_basic_headers(headers)
    assert any("Access-Control-Allow-Origin" in h for h in headers)


@pytest.mark.asyncio
async def test_get_headers_format():
    ws = Webserver("localhost", 8000)
    headers = await ws.get_headers(["A: 1"], "HTTP/1.1", 200)
    assert headers.startswith(b"HTTP/1.1 200")


@pytest.mark.asyncio
async def test_get_response_options():
    ws = Webserver("localhost", 8000)
    ws.response_protocol = "HTTP/1.1"
    ws.lowercase_headers = {}
    headers = await ws.get_response("OPTIONS", transport=None)
    assert any("Access-Control-Allow-Origin" in h for h in headers)


@pytest.mark.asyncio
async def test_get_response_get_and_post(monkeypatch):
    ws = Webserver("localhost", 8000)
    ws.path = "/"
    ws.response_protocol = "HTTP/1.1"
    ws.lowercase_headers = {}
    ws.cookies = {}
    ws.session = {}
    ws.request = ""
    ws.request_raw = b""
    ws.content_raw = b""
    ws.router_handler = AsyncMock()
    mock_resp = MagicMock()
    mock_resp.http_code = Constant.HTTP_OK
    mock_resp.content_type = "text/plain"
    mock_resp.headers = {}
    mock_resp.content = "hi"
    ws.router_handler.resolve.return_value = mock_resp
    ws.get_content_length = AsyncMock(return_value=0)
    result = await ws.get_response("GET", transport=None)
    assert isinstance(result, (bytes, bytearray))

    ws.get_content_length = AsyncMock(return_value=0)
    result = await ws.get_response("POST", transport=None)
    assert isinstance(result, (bytes, bytearray))


@pytest.mark.asyncio
async def test_handle_client_static_file(tmp_path, monkeypatch):
    # Create fake static file
    static_dir = tmp_path / "src" / "public"
    static_dir.mkdir(parents=True)
    file_path = static_dir / "file.txt"
    file_path.write_text("hello")
    tina4_python.root_path = str(tmp_path)

    ws = Webserver("localhost", 8000)
    ws.response_protocol = "HTTP/1.1"

    async def fake_get_data(reader):
        return "GET /file.txt HTTP/1.1", {}, {}, "", b"raw", b""

    ws.get_data = fake_get_data
    writer = MagicMock()
    writer.write = MagicMock()
    writer.drain = AsyncMock()
    writer.close = MagicMock()
    await ws.handle_client(None, writer)
    assert writer.write.called


@pytest.mark.asyncio
async def test_handle_client_error_path(monkeypatch):
    ws = Webserver("localhost", 8000)
    ws.response_protocol = "HTTP/1.1"

    async def fake_get_data(reader):
        raise Exception("boom")

    ws.get_data = fake_get_data
    monkeypatch.setattr(tina4_python, "global_exception_handler", lambda e: "error!")
    monkeypatch.setattr(tina4_python.Router, "clean_url", lambda u: u)
    monkeypatch.setattr(tina4_python.Template, "render_twig_template", lambda t, d: "html")
    writer = MagicMock()
    writer.write = MagicMock()
    writer.drain = AsyncMock()
    writer.close = MagicMock()
    await ws.handle_client(None, writer)
    assert writer.write.called
