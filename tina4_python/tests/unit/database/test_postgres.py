import pytest
import datetime
from tina4_python.Database import Database
from tina4_python.DatabaseTypes import POSTGRES
import psycopg2

@pytest.fixture(scope="module")
def db():
    # Correct format: driver:host/port:database
    return Database("psycopg2:localhost/5432:test_db", "postgres", "secret")

# DBMAIN-001: Postgres connection
def test_DBMAIN_001_postgres_connection(db):
    assert db.database_engine == POSTGRES
    assert db.dba is not None


def test_DBMAIN_003_table_exists_true(db):
    db.execute("DROP TABLE IF EXISTS test_table_exists CASCADE")
    db.execute("CREATE TABLE test_table_exists (id SERIAL PRIMARY KEY)")
    db.commit()
    assert db.table_exists("test_table_exists") is True


def test_DBMAIN_004_fetch_records(db):
    db.execute("CREATE TABLE IF NOT EXISTS test_fetch (id INTEGER, name TEXT)")
    db.execute("DELETE FROM test_fetch")
    db.insert("test_fetch", [{"id": 1, "name": "Alpha"}, {"id": 2, "name": "Beta"}])
    db.commit()
    result = db.fetch("SELECT * FROM test_fetch ORDER BY id", limit=2)
    assert result.count == 2

def test_DBMAIN_005_fetch_one_record(db):
    record = db.fetch_one("SELECT * FROM test_fetch WHERE id = ?", [1])
    assert record["name"] == "Alpha"

def test_DBMAIN_006_execute_insert(db):
    result = db.execute("INSERT INTO test_fetch (id, name) VALUES (?, ?)", [3, "Gamma"])
    db.commit()
    assert result.error is None

def test_DBMAIN_007_execute_update(db):
    result = db.execute("UPDATE test_fetch SET name = ? WHERE id = ?", ["Updated", 3])
    db.commit()
    assert result.error is None

def test_DBMAIN_008_execute_delete(db):
    result = db.execute("DELETE FROM test_fetch WHERE id = ?", [3])
    db.commit()
    assert result.error is None

def test_DBMAIN_009_transaction_commit(db):
    db.start_transaction()
    db.insert("test_fetch", {"id": 4, "name": "Temp"})
    db.commit()
    record = db.fetch_one("SELECT * FROM test_fetch WHERE id = 4")
    assert record["name"] == "Temp"

def test_DBMAIN_010_data_type_conversion_datetime(db):
    now = datetime.datetime.now()
    db.execute("CREATE TABLE IF NOT EXISTS test_dates (id INTEGER, created TIMESTAMP)")
    db.execute("DELETE FROM test_dates")
    db.execute("INSERT INTO test_dates (id, created) VALUES (?, ?)", [1, now])
    db.commit()
    record = db.fetch_one("SELECT * FROM test_dates WHERE id = ?", [1])
    created = record["created"]

    if isinstance(created, str):
        assert "T" in created or " " in created
    elif isinstance(created, int):
        assert created > 0
    elif isinstance(created, datetime.datetime):
        assert created.year == now.year
        assert created.month == now.month
        assert created.day == now.day
    else:
        pytest.fail(f"Unexpected datetime format: {type(created)}")

def test_DBMAIN_011_insert_method(db):
    result = db.insert("test_fetch", {"id": 6, "name": "InsertAPI"})
    db.commit()
    assert result.error is None

def test_DBMAIN_012_update_method(db):
    result = db.update("test_fetch", {"id": 6, "name": "UpdatedAPI"})
    db.commit()
    assert result is True

def test_DBMAIN_013_delete_method(db):
    result = db.delete("test_fetch", {"id": 6})
    db.commit()
    assert result is True

def test_DBMAIN_014_get_next_id(db):
    db.execute("CREATE TABLE IF NOT EXISTS next_id_test (id INTEGER PRIMARY KEY)")
    db.execute("DELETE FROM next_id_test")
    db.commit()
    db.insert("next_id_test", {"id": 10})
    db.commit()
    assert db.get_next_id("next_id_test") == 11

def test_DBMAIN_015_invalid_connection_string():
    with pytest.raises(SystemExit):
        Database("invalid_driver:some/connection")

def test_DBMAIN_016_table_exists_false(db):
    db.execute("DROP TABLE IF EXISTS non_existent_table")
    db.commit()
    assert db.table_exists("non_existent_table") is False

def test_DBMAIN_017_fetch_invalid_sql(db):
    result = db.fetch("SELECT * FROM does_not_exist")
    assert result.error is not None

def test_DBMAIN_018_execute_invalid_sql(db):
    result = db.execute("INVALID SQL")
    assert result.error is not None

def test_DBMAIN_019_transaction_rollback(db):
    db.start_transaction()
    db.insert("test_fetch", {"id": 5, "name": "ShouldNotExist"})
    db.rollback()
    record = db.fetch_one("SELECT * FROM test_fetch WHERE id = 5")
    assert record is None

def test_DBMAIN_020_fetch_one_empty_result(db):
    record = db.fetch_one("SELECT * FROM test_fetch WHERE id = ?", [999])
    assert record is None

def test_DBMAIN_021_insert_invalid_data(db):
    result = db.insert("test_fetch", "invalid_input")
    assert result is False or result is None

def test_DBMAIN_022_update_non_existent(db):
    result = db.update("test_fetch", {"id": 999, "name": "Ghost"})
    db.commit()
    assert isinstance(result, bool)

def test_DBMAIN_023_delete_non_existent(db):
    result = db.delete("test_fetch", {"id": 999})
    assert isinstance(result, bool)

def test_DBMAIN_024_get_next_id_empty_table(db):
    db.execute("DELETE FROM next_id_test")
    db.commit()
    assert db.get_next_id("next_id_test") == 1
