import os
import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
pytestmark = pytest.mark.asyncio


from tina4_python.Websocket import Websocket


class DummyRequest:
    def __init__(self, asgi_response=False, headers=None, transport=None):
        self.asgi_response = asgi_response
        self.headers = headers or {}
        self.transport = transport

# WS-001: Successful ASGI connection
@pytest.mark.asyncio
async def test_ws_asgi_connection_success():
    mock_server = MagicMock()
    mock_server.AioServer.accept = AsyncMock(return_value="ASGI-CONNECTION")

    request = DummyRequest(asgi_response=True, transport="fake-transport")

    with patch("tina4_python.Websocket.importlib.import_module", return_value=mock_server):
        ws = Websocket(request)
        result = await ws.connection()
        assert result == "ASGI-CONNECTION"
        mock_server.AioServer.accept.assert_awaited_once_with(asgi="fake-transport")


# WS-002: Successful socket connection (Windows)
@pytest.mark.asyncio
async def test_ws_socket_connection_windows():
    mock_server = MagicMock()
    mock_server.AioServer.accept = AsyncMock(return_value="SOCKET-WIN-CONNECTION")

    mock_sock = object()
    mock_transport = MagicMock()
    mock_transport.transport._sock = mock_sock

    request = DummyRequest(asgi_response=False, transport=mock_transport, headers={"Auth": "token"})

    with patch("os.name", "nt"):
        with patch("tina4_python.Websocket.importlib.import_module", return_value=mock_server):
            ws = Websocket(request)
            result = await ws.connection()
            assert result == "SOCKET-WIN-CONNECTION"
            mock_server.AioServer.accept.assert_awaited_once()


# WS-003: Successful socket connection (Non-Windows)
@pytest.mark.asyncio
async def test_ws_socket_connection_non_windows():
    mock_server = MagicMock()
    mock_server.AioServer.accept = AsyncMock(return_value="SOCKET-LINUX-CONNECTION")

    mock_socket = MagicMock()
    mock_socket.dup.return_value = "DUPLICATED-SOCKET"
    mock_transport = MagicMock()
    mock_transport.get_extra_info.return_value = mock_socket

    request = DummyRequest(asgi_response=False, transport=mock_transport, headers={"Auth": "token"})

    with patch("os.name", "posix"):
        with patch("tina4_python.Websocket.importlib.import_module", return_value=mock_server):
            ws = Websocket(request)
            result = await ws.connection()
            assert result == "SOCKET-LINUX-CONNECTION"
            mock_server.AioServer.accept.assert_awaited_once_with(
                sock="DUPLICATED-SOCKET",
                headers={"Auth": "token"}
            )


# WS-004: Missing simple_websocket module
def test_ws_import_error_logs():
    with patch("tina4_python.Websocket.importlib.import_module", side_effect=ImportError("no module")):
        with patch("tina4_python.Websocket.Debug.error") as mock_debug:
            ws = Websocket(DummyRequest())
            mock_debug.assert_called_once()
            assert hasattr(ws, "request")
# WS-005: Exception during accept()
@pytest.mark.asyncio
async def test_ws_accept_error_returns_none():
    mock_server = MagicMock()
    mock_server.AioServer.accept = AsyncMock(side_effect=Exception("accept fail"))

    request = DummyRequest(asgi_response=True, transport="fake-transport")

    with patch("tina4_python.Websocket.importlib.import_module", return_value=mock_server):
        with patch("tina4_python.Websocket.Debug.error") as mock_debug:
            ws = Websocket(request)
            result = await ws.connection()
            assert result is None
            mock_debug.assert_called_once()
