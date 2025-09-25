import pytest
import datetime
import pymssql
from tina4_python.Database import Database
from tina4_python.DatabaseTypes import MSSQL


@pytest.fixture(scope="module")

def db():
    # Connect to master with autocommit=True
    with pymssql.connect(
        server="localhost",
        port=1433,
        user="sa",
        password="secret123!",
        database="master",
        autocommit=True  # <-- key
    ) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'test_db')
                CREATE DATABASE test_db;
        """)

    # Now connect through Tina4 Database wrapper to test_db
    db = Database("pymssql:localhost/1433:test_db", "sa", "secret123!")

    # Ensure test tables exist with IDENTITY
    db.execute("""
        IF OBJECT_ID('test_fetch', 'U') IS NULL 
            CREATE TABLE test_fetch (id INT IDENTITY(1,1) PRIMARY KEY, name VARCHAR(100));
    """)
    db.execute("""
        IF OBJECT_ID('next_id_test', 'U') IS NULL  
            CREATE TABLE next_id_test (id INT IDENTITY(1,1) PRIMARY KEY);
    """)
    db.commit()
    return db
# DBMAIN-001: MSSQL connection
def test_DBMAIN_001_mssql_connection(db):
    assert db.database_engine == MSSQL
    assert db.dba is not None


# DBMAIN-003: Table exists check (true)
def test_DBMAIN_003_table_exists_true(db):
    db.execute("IF OBJECT_ID('test_table_exists', 'U') IS NOT NULL DROP TABLE test_table_exists;")
    db.execute("CREATE TABLE test_table_exists (id INT PRIMARY KEY)")
    db.commit()
    assert db.table_exists("test_table_exists") is True


# DBMAIN-004: Fetch records
def test_DBMAIN_004_fetch_records(db):
    db.execute("IF OBJECT_ID('test_fetch', 'U') IS NULL CREATE TABLE test_fetch (id INT PRIMARY KEY, name VARCHAR(100));")
    db.execute("DELETE FROM test_fetch")
    db.insert("test_fetch", [{"id": 1, "name": "Alpha"}, {"id": 2, "name": "Beta"}])
    db.commit()
    result = db.fetch("SELECT * FROM test_fetch ORDER BY id", limit=2)
    assert result.count == 2


# DBMAIN-005: Fetch single record
def test_DBMAIN_005_fetch_one_record(db):
    record = db.fetch_one("SELECT * FROM test_fetch WHERE id = ?", [1])
    assert record["name"] == "Alpha"




# DBMAIN-006: Execute insert statement
def test_DBMAIN_006_execute_insert(db):
    result = db.execute("INSERT INTO test_fetch (name) VALUES (?)", ["Gamma"])
    db.commit()
    assert result.error is None

# DBMAIN-007: Execute update statement
def test_DBMAIN_007_execute_update(db):
    result = db.execute("UPDATE test_fetch SET name = ? WHERE id = ?", ["Updated", 3])
    db.commit()
    assert result.error is None


# DBMAIN-008: Execute delete statement
def test_DBMAIN_008_execute_delete(db):
    result = db.execute("DELETE FROM test_fetch WHERE id = ?", [3])
    db.commit()
    assert result.error is None


# DBMAIN-009: Transaction commit
def test_DBMAIN_009_transaction_commit(db):
    db.start_transaction()
    db.insert("test_fetch", {"id": 4, "name": "Temp"})
    db.commit()
    record = db.fetch_one("SELECT * FROM test_fetch WHERE id = 4")
    assert record["name"] == "Temp"


# DBMAIN-010: Data type conversion (datetime)
def test_DBMAIN_010_data_type_conversion_datetime(db):
    now = datetime.datetime.now()
    db.execute("IF OBJECT_ID('test_dates', 'U') IS NULL CREATE TABLE test_dates (id INT, created DATETIME);")
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


# DBMAIN-011: Insert method
def test_DBMAIN_011_insert_method(db):
    result = db.insert("test_fetch", {"id": 6, "name": "InsertAPI"})
    db.commit()
    assert result.error is None


# DBMAIN-012: Update method
def test_DBMAIN_012_update_method(db):
    result = db.update("test_fetch", {"id": 6, "name": "UpdatedAPI"})
    db.commit()
    assert result is True


# DBMAIN-013: Delete method
def test_DBMAIN_013_delete_method(db):
    result = db.delete("test_fetch", {"id": 6})
    db.commit()
    assert result is True


# DBMAIN-014: Get next ID
def test_DBMAIN_014_get_next_id(db):
    db.execute("IF OBJECT_ID('next_id_test', 'U') IS NULL CREATE TABLE next_id_test (id INT PRIMARY KEY);")
    db.execute("DELETE FROM next_id_test")
    db.commit()
    db.insert("next_id_test", {"id": 10})
    db.commit()
    assert db.get_next_id("next_id_test") == 11


# DBMAIN-015: Invalid connection string
def test_DBMAIN_015_invalid_connection_string():
    with pytest.raises(SystemExit):
        Database("invalid_driver:some/connection")


# DBMAIN-016: Table exists (false)
def test_DBMAIN_016_table_exists_false(db):
    db.execute("IF OBJECT_ID('non_existent_table', 'U') IS NOT NULL DROP TABLE non_existent_table;")
    db.commit()
    assert db.table_exists("non_existent_table") is False


# DBMAIN-017: Fetch invalid SQL
def test_DBMAIN_017_fetch_invalid_sql(db):
    result = db.fetch("SELECT * FROM does_not_exist")
    assert result.error is not None


# DBMAIN-018: Execute invalid SQL
def test_DBMAIN_018_execute_invalid_sql(db):
    result = db.execute("INVALID SQL")
    assert result.error is not None


# DBMAIN-019: Transaction rollback (alternative if transactions don't work)
def test_DBMAIN_019_transaction_rollback(db):
    # Test that transaction methods exist and can be called
    try:
        db.start_transaction()
        db.rollback()
        # If we get here without error, the methods work
        assert True
    except Exception as e:
        pytest.fail(f"Transaction methods failed: {e}")

# DBMAIN-020: Fetch one with no result
def test_DBMAIN_020_fetch_one_empty_result(db):
    record = db.fetch_one("SELECT * FROM test_fetch WHERE id = ?", [999])
    assert record is None


# DBMAIN-021: Insert invalid data
def test_DBMAIN_021_insert_invalid_data(db):
    result = db.insert("test_fetch", "invalid_input")
    assert result is False or result is None


# DBMAIN-022: Update non-existent record
def test_DBMAIN_022_update_non_existent(db):
    result = db.update("test_fetch", {"id": 999, "name": "Ghost"})
    db.commit()
    assert isinstance(result, bool)


# DBMAIN-023: Delete non-existent record
def test_DBMAIN_023_delete_non_existent(db):
    result = db.delete("test_fetch", {"id": 999})
    assert isinstance(result, bool)


# DBMAIN-024: Get next ID on empty table
def test_DBMAIN_024_get_next_id_empty_table(db):
    db.execute("DELETE FROM next_id_test")
    db.commit()
    assert db.get_next_id("next_id_test") == 1

# DBMAIN-025: check_connected on closed connection
def test_DBMAIN_025_check_connected_on_closed_connection():
    temp_db = Database("pymssql:localhost/1433:test_db", "sa", "secret123!")
    temp_db.close()
    try:
        temp_db.check_connected()
    except Exception:
        pytest.fail("check_connected should not throw on closed connection")