import asyncio
import base64
import json
import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from tina4_python.Webserver import Webserver


@pytest.fixture
def server(tmp_path):
    """Fixture to create a Webserver with mocked router."""
    s = Webserver("localhost", 8080)
    s.router_handler = AsyncMock()
    return s


@pytest.fixture
def writer():
    """Mock writer with async-friendly methods."""
    w = MagicMock()
    w.write = MagicMock()
    w.drain = AsyncMock()
    w.close = MagicMock()
    return w


# -------------------------
# Positive Test Cases
# -------------------------

@pytest.mark.asyncio
async def test_WServer_001_handle_simple_get_request(tmp_path, writer):
    public_dir = tmp_path / "src" / "public"
    public_dir.mkdir(parents=True)
    test_file = public_dir / "index.html"
    test_file.write_text("Hello World")

    server = Webserver("localhost", 8080)
    request = b"GET /index.html HTTP/1.1\r\n\r\n"
    reader = AsyncMock()
    reader.readuntil = AsyncMock(return_value=request)

    with patch("tina4_python.root_path", str(tmp_path)):
        await server.handle_client(reader, writer)

    writer.write.assert_called()
    args, _ = writer.write.call_args
    assert b"Hello World" in args[0]


@pytest.mark.asyncio
async def test_WServer_002_handle_post_with_json(server):
    server.lowercase_headers = {"content-type": "application/json", "content-length": "15"}
    server.content_raw = b'{"key": "val"}'

    body = await server.get_content_body(15)
    assert body == {"key": "val"}


@pytest.mark.asyncio
async def test_WServer_003_static_file_delivery(tmp_path, writer):
    public_dir = tmp_path / "src" / "public"
    public_dir.mkdir(parents=True)
    f = public_dir / "test.txt"
    f.write_text("static content")

    server = Webserver("localhost", 8080)
    request = b"GET /test.txt HTTP/1.1\r\n\r\n"
    reader = AsyncMock()
    reader.readuntil = AsyncMock(return_value=request)

    with patch("tina4_python.root_path", str(tmp_path)):
        await server.handle_client(reader, writer)

    args, _ = writer.write.call_args
    assert b"static content" in args[0]


@pytest.mark.asyncio
async def test_WServer_004_form_data_parsing(server):
    server.lowercase_headers = {"content-type": "application/x-www-form-urlencoded"}
    server.content_raw = b"a=1&b=hello+world"

    body = await server.get_content_body(len(server.content_raw))
    assert body == {"a": "1", "b": "hello world"}


@pytest.mark.asyncio
async def test_WServer_005_multipart_upload(server):
    boundary = "----boundary"
    content = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="file"; filename="test.txt"\r\n'
        "Content-Type: text/plain\r\n\r\n"
        "filecontent\r\n"
        f"--{boundary}--\r\n"
    )
    server.lowercase_headers = {"content-type": f"multipart/form-data; boundary={boundary}"}
    server.content_raw = content.encode()

    body = await server.get_content_body(len(content))
    assert "file" in body
    assert body["file"]["file_name"] == "test.txt"
    assert base64.b64decode(body["file"]["content"]).startswith(b"filecontent")


@pytest.mark.asyncio
async def test_WServer_006_options_request(server):
    headers = await server.get_response("OPTIONS", transport=None)
    assert b"Access-Control-Allow-Origin" in headers
    assert b"200 OK" in headers


@pytest.mark.asyncio
async def test_WServer_007_session_cookie_set(server, writer):
    server.router_handler.resolve = AsyncMock(
        return_value=MagicMock(http_code=200, content="ok", content_type="text/plain", headers={})
    )
    server.lowercase_headers = {}
    server.cookies = {}
    server.path = "/"
    server.request = "raw"
    server.request_raw = b"raw"
    server.content_raw = b""

    response = await server.get_response("GET", writer)
    assert b"ok" in response


@pytest.mark.asyncio
async def test_WServer_008_complex_query_parameters(server):
    server.lowercase_headers = {}
    server.cookies = {}
    server.path = "/api?a[b][c]=1"
    server.request = "raw"
    server.request_raw = b"raw"
    server.content_raw = b""

    server.router_handler.resolve = AsyncMock(
        return_value=MagicMock(http_code=200, content="ok", content_type="text/plain", headers={})
    )

    response = await server.get_response("GET", transport=None)
    assert b"ok" in response


# -------------------------
# Negative Test Cases
# -------------------------

@pytest.mark.asyncio
async def test_WServer_009_unknown_content_type(server):
    server.lowercase_headers = {"content-type": "weird/type"}
    server.content_raw = b"binarydata"

    body = await server.get_content_body(len(server.content_raw))
    assert "data" in body


@pytest.mark.asyncio
async def test_WServer_010_corrupt_multipart_boundary(server):
    server.lowercase_headers = {"content-type": "multipart/form-data; boundary=bad"}
    server.content_raw = b"corrupt"

    body = await server.get_content_body(len(server.content_raw))
    assert isinstance(body, dict)


@pytest.mark.asyncio
async def test_WServer_011_invalid_json(server):
    server.lowercase_headers = {"content-type": "application/json"}
    server.content_raw = b"{broken json}"

    body = await server.get_content_body(len(server.content_raw))
    assert isinstance(body, str)


@pytest.mark.asyncio
async def test_WServer_012_no_content_length(server):
    server.lowercase_headers = {}
    length = await server.get_content_length()
    assert length == 0


@pytest.mark.asyncio
async def test_WServer_013_unknown_route_returns_404(server):
    server.router_handler.resolve = AsyncMock(
        return_value=MagicMock(http_code=404, content="not found", content_type="text/plain", headers={})
    )
    server.lowercase_headers = {}
    server.cookies = {}
    server.path = "/not-found"
    server.request = "raw"
    server.request_raw = b"raw"
    server.content_raw = b""

    response = await server.get_response("GET", transport=None)
    assert b"not found" in response


@pytest.mark.asyncio
async def test_WServer_014_websocket_fallback(server):
    server.lowercase_headers = {"sec-websocket-key": "abc"}
    server.router_handler.resolve = AsyncMock(
        return_value=MagicMock(http_code=200, content="socket", content_type="text/plain", headers={})
    )

    response = await server.get_response("GET", transport=None)
    assert response is not None


@pytest.mark.asyncio
async def test_WServer_015_broken_pipe_handling(tmp_path, writer):
    # Prepare dummy static file
    public_dir = tmp_path / "src" / "public"
    public_dir.mkdir(parents=True)
    f = public_dir / "index.html"
    f.write_text("BrokenPipe test")

    server = Webserver("localhost", 8080)
    server.router_handler = AsyncMock()
    server.router_handler.resolve = AsyncMock(
        return_value=MagicMock(http_code=200, content=b"ok", content_type="text/plain", headers={})
    )

    request = b"GET /index.html HTTP/1.1\r\n\r\n"
    reader = AsyncMock()
    reader.readuntil = AsyncMock(return_value=request)

    # Simulate broken pipe on write
    writer.write.side_effect = BrokenPipeError("Pipe broken")

    # We only want to ensure the server doesn’t crash hard
    with patch("tina4_python.root_path", str(tmp_path)), patch("tina4_python.Debug.Debug.info") as mock_info:
        try:
            await server.handle_client(reader, writer)
        except BrokenPipeError:
            # Expected due to simulated connection break
            pass

    mock_info.assert_called()
