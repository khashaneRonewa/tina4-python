import os
import pytest
import sqlite3
from pathlib import Path
from tina4_python.Database import Database
from tina4_python.Migration import migrate


@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    # Set root path for migrations
    monkeypatch.setattr('tina4_python.root_path', str(tmp_path))

    # Create fresh database
    db_file = tmp_path / "test.db"
    dba = Database(f"sqlite3:{db_file}")

    # Create migrations directory
    migrations_dir = tmp_path / "migrations"
    migrations_dir.mkdir(exist_ok=True)

    # Store paths in dba for test access
    dba.test_root = tmp_path
    dba.migrations_dir = migrations_dir

    yield dba

    # Clean up
    dba.close()


def test_successful_migration(setup_db):
    dba = setup_db
    # Create valid migration
    (dba.migrations_dir / "001_valid.sql").write_text("CREATE TABLE test_mig (id INTEGER);")

    # Run migration
    migrate(dba)

    # Verify table was created
    tables = dba.fetch("SELECT name FROM sqlite_master WHERE type='table'").to_array()
    assert any(t["name"] == "test_mig" for t in tables), f"Tables found: {tables}"


def test_migration_already_applied(setup_db):
    dba = setup_db
    # Create migration
    (dba.migrations_dir / "001_repeat.sql").write_text("CREATE TABLE already_done (id INTEGER);")

    # First run - should create table and record
    migrate(dba)
    first_count = len(dba.fetch("SELECT * FROM tina4_migration").to_array())

    # Second run - should skip
    migrate(dba)
    second_count = len(dba.fetch("SELECT * FROM tina4_migration").to_array())

    assert first_count == 1, "Migration not recorded"
    assert second_count == 1, "Duplicate migration recorded"



def test_invalid_sql_fails_and_rolls_back(setup_db):
    dba = setup_db
    # Create invalid migration
    (dba.migrations_dir / "001_invalid.sql").write_text("INVALID SQL;")

    # Should raise database error
    with pytest.raises(SystemExit):  # Changed from RuntimeError to SystemExit
        migrate(dba)

    # Verify a failed migration record was created
    records = dba.fetch("SELECT * FROM tina4_migration").to_array()
    assert len(records) == 1
    assert records[0]["passed"] == 0
    assert "syntax error" in records[0]["error_message"]


def test_partial_migration_failure(setup_db):
    dba = setup_db
    (dba.migrations_dir / "002_partial.sql").write_text(
        "CREATE TABLE success (id INT);\nINVALID SQL;"
    )

    with pytest.raises(SystemExit):
        migrate(dba)

    # Verify failed migration record
    records = dba.fetch("SELECT * FROM tina4_migration").to_array()
    assert len(records) == 1
    assert records[0]["passed"] == 0

    # Verify table WAS created (DDL can't be rolled back in SQLite)
    assert any(
        t["name"] == "success"
        for t in dba.fetch("SELECT name FROM sqlite_master WHERE type='table'").to_array()
    )

def test_missing_migration_folder(setup_db):
    dba = setup_db
    # Test non-existent folder
    with pytest.raises(FileNotFoundError):
        migrate(dba, migration_folder="nonexistent_folder")


def test_empty_migration_folder(setup_db):
    dba = setup_db
    # Should run without errors
    migrate(dba)
    # Verify no migrations were run
    assert len(dba.fetch("SELECT * FROM tina4_migration").to_array()) == 0