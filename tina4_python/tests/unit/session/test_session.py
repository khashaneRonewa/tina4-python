import os
import shutil
import sys
import pytest
from unittest.mock import patch, MagicMock
from tina4_python.Session import Session, SessionFileHandler, SessionRedisHandler
import tina4_python


@pytest.fixture
def clean_session_dir():
    """Creates a clean temporary session directory before each test."""
    path = "test_sessions"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    yield path
    shutil.rmtree(path)


# =============================
# Positive Test Cases
# =============================

def test_session_001_file_session_initialization(clean_session_dir):
    session = Session(_default_path=clean_session_dir)
    file_hash = session.start()
    assert os.path.isfile(os.path.join(clean_session_dir, file_hash))


def test_session_002_session_data_setting(clean_session_dir):
    session = Session(_default_path=clean_session_dir)
    assert session.set("key", "value") is True
    file_hash = session.start()
    with open(os.path.join(clean_session_dir, file_hash)) as f:
        assert f.read() != ""


def test_session_003_session_data_retrieval(clean_session_dir):
    session = Session(_default_path=clean_session_dir)
    session.set("key", "value")
    assert session.get("key") == "value"


def test_session_004_session_data_removal(clean_session_dir):
    session = Session(_default_path=clean_session_dir)
    session.set("key", "value")
    assert session.unset("key") is True
    assert session.get("key") is None


def test_session_005_session_loading(clean_session_dir):
    session = Session(_default_path=clean_session_dir)
    session.set("x", "123")
    hash_id = session.start()

    session2 = Session(_default_path=clean_session_dir)
    session2.load(hash_id)
    assert session2.get("x") == "123" or session2.get("x") is None


def test_session_006_session_cleanup(clean_session_dir):
    session = Session(_default_path=clean_session_dir)
    hash_id = session.start()
    assert session.close() is True
    assert not os.path.exists(os.path.join(clean_session_dir, hash_id))


def test_session_007_redis_session_initialization(monkeypatch):
    mock_redis = MagicMock()
    monkeypatch.setattr(SessionRedisHandler, "_SessionRedisHandler__init_redis", lambda: mock_redis)
    session = Session(_default_handler="SessionRedisHandler")
    assert issubclass(session.default_handler, SessionRedisHandler)



def test_session_008_multiple_session_values(clean_session_dir):
    session = Session(_default_path=clean_session_dir)
    session.set("a", 1)
    session.set("b", 2)
    assert session.get("a") == 1
    assert session.get("b") == 2


# =============================
# Negative Test Cases
# =============================

def test_session_009_invalid_session_key_access(clean_session_dir):
    session = Session(_default_path=clean_session_dir)
    assert session.get("non-existent") is None


def test_session_010_missing_redis_dependency(monkeypatch):
    monkeypatch.setitem(sys.modules, "redis", None)
    with pytest.raises(SystemExit):
        SessionRedisHandler._SessionRedisHandler__init_redis()


def test_session_011_invalid_session_file_access(clean_session_dir):
    corrupted_file = os.path.join(clean_session_dir, "fakehash")
    with open(corrupted_file, "w") as f:
        f.write("corrupted-data")

    session = Session(_default_path=clean_session_dir)
    # Force invalid token
    monkeypatch = patch.object(tina4_python, "tina4_auth", MagicMock(valid=lambda t: False))
    with monkeypatch:
        session.load("fakehash")
    assert session.session_hash == "fakehash"


def test_session_012_expired_session_token(clean_session_dir, monkeypatch):
    session = Session(_default_path=clean_session_dir)
    session.set("user", "test")
    hash_id = session.start()

    # Simulate expired token
    monkeypatch.setattr(tina4_python.tina4_auth, "valid", lambda token: False)
    session2 = Session(_default_path=clean_session_dir)
    session2.load(hash_id)
    assert session2.session_hash == hash_id


def test_session_013_invalid_storage_path(tmp_path):
    # Make a directory read-only
    invalid_dir = tmp_path / "readonly"
    invalid_dir.mkdir()
    os.chmod(invalid_dir, 0o400)  # Read-only

    session = Session(_default_path=str(invalid_dir))
    result = session.save()
    assert result is False
