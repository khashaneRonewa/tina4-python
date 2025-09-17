import os
import pytest
import datetime
from tina4_python.Database import Database
from tina4_python.DatabaseTypes import FIREBIRD

DSN = f"localhost/3050:/var/lib/firebird/data/testdb.fdb"
DB_USER = "SYSDBA"
DB_PASS = "masterkey"

@pytest.fixture(scope="module")
def db():
    # Now connect via Tina4 Database wrapper (must use fdb:)
    db = Database(f"firebird.driver:{DSN}", DB_USER, DB_PASS)

    # Ensure test tables exist
    for ddl in [
        "DROP TABLE test_fetch",
        "DROP TABLE test_table_exists",
        "DROP TABLE next_id_test",
        "DROP TABLE test_dates",
    ]:
        try:
            db.execute(ddl)
            db.commit()
        except Exception:
            pass

    db.execute("CREATE TABLE test_fetch (id INTEGER PRIMARY KEY, name VARCHAR(100))")
    db.execute("CREATE TABLE test_table_exists (id INTEGER PRIMARY KEY)")
    db.execute("CREATE TABLE next_id_test (id INTEGER PRIMARY KEY)")
    db.execute("CREATE TABLE test_dates (id INTEGER, created TIMESTAMP)")
    db.commit()
    return db


# DBMAIN-001: Firebird connection
def test_DBMAIN_001_firebird_connection(db):
    assert db.database_engine == FIREBIRD
    assert db.dba is not None


