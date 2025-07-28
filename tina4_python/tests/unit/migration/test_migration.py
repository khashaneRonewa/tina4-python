import os
import sys
import pytest
from unittest.mock import patch, MagicMock, call
from pathlib import Path
from tina4_python.Migration import migrate
from tina4_python.Database import MSSQL, POSTGRES, FIREBIRD, MYSQL


def create_migration_file(tmpdir, filename, content):
    migrations_dir = tmpdir / "migrations"
    migrations_dir.mkdir(parents=True, exist_ok=True)
    file_path = migrations_dir / filename
    file_path.write_text(content)
    return migrations_dir


class MockResult:
    def __init__(self, error=None):
        self.error = error


@pytest.fixture
def fake_dba():
    dba = MagicMock()
    dba.database_engine = "sqlite3"
    dba.table_exists.return_value = False
    dba.get_next_id.return_value = 1
    dba.execute.return_value = MockResult()
    dba.fetch.return_value = []
    dba.commit = MagicMock()
    dba.rollback = MagicMock()
    return dba


def test_generic_table_creation_sqlite(fake_dba, tmp_path):
    os.environ["TINA4_ROOT_PATH"] = str(tmp_path)
    create_migration_file(tmp_path, "001_init.sql", "CREATE TABLE test (id INTEGER);")
    migrate(fake_dba)
    fake_dba.execute.assert_called()


def test_successful_migration(fake_dba, tmp_path):
    os.environ["TINA4_ROOT_PATH"] = str(tmp_path)
    create_migration_file(tmp_path, "001_success.sql", "CREATE TABLE test_mig (id INTEGER);")

    # Setup mock responses
    fake_dba.fetch.side_effect = [
        [],  # First check for existing migration
        [{"max": 1}],  # get_next_id response
        []  # Final insert check
    ]

    # Setup execute responses
    ok_result = MockResult()
    fake_dba.execute.side_effect = [
        ok_result,  # create tina4_migration table
        ok_result,  # delete any failed migration record
        ok_result,  # execute migration SQL
        ok_result  # insert migration record
    ]

    # Reset commit mock
    fake_dba.commit.reset_mock()

    migrate(fake_dba)

    # Verify commit was called at least twice (after delete and after insert)
    assert fake_dba.commit.call_count >= 2


def test_empty_migration_folder(fake_dba, tmp_path):
    os.environ["TINA4_ROOT_PATH"] = str(tmp_path)
    (tmp_path / "migrations").mkdir()
    migrate(fake_dba)
    assert True  # no crash


def test_migration_already_applied(fake_dba, tmp_path):
    os.environ["TINA4_ROOT_PATH"] = str(tmp_path)
    create_migration_file(tmp_path, "001_repeat.sql", "CREATE TABLE already_done (id INTEGER);")

    # Mock response showing migration already applied
    fake_dba.fetch.return_value = [{"description": "001_repeat.sql", "passed": 1}]

    # Reset fetch mock to track calls
    fake_dba.fetch.reset_mock()

    migrate(fake_dba)

    # Verify fetch was called to check migration status
    assert fake_dba.fetch.call_count >= 1


def test_invalid_sql_fails_and_rolls_back(fake_dba, tmp_path):
    os.environ["TINA4_ROOT_PATH"] = str(tmp_path)
    create_migration_file(tmp_path, "001_invalid.sql", "INVALID SQL SYNTAX;")

    # Setup mocks
    fake_dba.table_exists.return_value = True
    fake_dba.fetch.side_effect = [
        [],  # First check for existing migration
        [{"max": 1}]  # get_next_id response
    ]

    # First two calls succeed, third fails
    fake_dba.execute.side_effect = [
        MockResult(),  # create table if not exists
        MockResult(),  # delete existing failed migration
        MockResult(error="Syntax error")  # execute migration (fails)
    ]

    # Reset rollback mock
    fake_dba.rollback.reset_mock()

    with patch("sys.exit") as mock_exit:
        migrate(fake_dba)
        assert fake_dba.rollback.call_count >= 1
        mock_exit.assert_called_once()


def test_partial_migration_failure(fake_dba, tmp_path):
    os.environ["TINA4_ROOT_PATH"] = str(tmp_path)
    create_migration_file(tmp_path, "002_partial_fail.sql", "CREATE TABLE ok (id INT); INVALID SQL;")

    # Setup mocks
    fake_dba.table_exists.return_value = True
    fake_dba.fetch.side_effect = [
        [],  # First check for existing migration
        [{"max": 1}]  # get_next_id response
    ]

    # First three calls succeed, fourth fails
    fake_dba.execute.side_effect = [
        MockResult(),  # create table if not exists
        MockResult(),  # delete existing failed migration
        MockResult(),  # first valid statement
        MockResult(error="SQL error")  # second invalid statement
    ]

    # Reset rollback mock
    fake_dba.rollback.reset_mock()

    with patch("sys.exit") as mock_exit:
        migrate(fake_dba)
        assert fake_dba.rollback.call_count >= 1
        mock_exit.assert_called_once()


def test_missing_migration_folder(fake_dba, tmp_path):
    bad_folder = tmp_path / "nonexistent"
    with patch("tina4_python.root_path", str(tmp_path)), patch("sys.exit") as mock_exit:
        migrate(fake_dba, migration_folder="nonexistent")
        mock_exit.assert_called_once()


@pytest.mark.parametrize("engine", [MSSQL, POSTGRES, MYSQL, FIREBIRD])
def test_engine_table_creation(engine, fake_dba, tmp_path):
    os.environ["TINA4_ROOT_PATH"] = str(tmp_path)
    fake_dba.database_engine = engine
    fake_dba.fetch.side_effect = [
        [],
        [{"max": 1}]
    ]
    create_migration_file(tmp_path, "init.sql", "CREATE TABLE something (id INT);")
    migrate(fake_dba)
    fake_dba.execute.assert_called()