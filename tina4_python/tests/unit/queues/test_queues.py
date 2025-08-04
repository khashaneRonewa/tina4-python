import pytest
from unittest.mock import MagicMock, patch
from tina4_python.Queue import Queue, Config, Message


@pytest.fixture
def mock_litequeue():
    mock_msg = MagicMock()
    mock_msg.message_id = "msg-001"
    mock_msg.data = '{"msg": "Hello", "user_id": "user123"}'
    mock_msg.status = 1
    mock_msg.in_time = 1720000000

    mock_queue = MagicMock()
    mock_queue.put.return_value = mock_msg
    mock_queue.pop.return_value = mock_msg
    mock_queue.get.return_value = mock_msg
    return mock_queue, mock_msg


def   test_produce_message_litequeue(mock_litequeue):
    mock_queue, mock_msg = mock_litequeue
    config = Config()
    config.queue_type = "litequeue"

    with patch("tina4_python.Queue.importlib.import_module") as mock_import:
        mock_import.return_value.LiteQueue.return_value = mock_queue
        q = Queue(config=config, topic="test-queue")
        result = q.produce("Hello", user_id="user123")

        assert isinstance(result, Message)
        assert result.message_id == "msg-001"
        assert result.data == "Hello"
        assert result.user_id == "user123"
        assert result.status == 1


def test_consume_message_litequeue(mock_litequeue):
    mock_queue, mock_msg = mock_litequeue
    config = Config()
    config.queue_type = "litequeue"

    consumed = []

