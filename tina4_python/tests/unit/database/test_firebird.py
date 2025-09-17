import os
import pytest
import datetime
import fdb
from tina4_python.Database import Database
from tina4_python.DatabaseTypes import FIREBIRD

DB_FILE = "/home/database/TEST.FDB"
DSN = f"localhost/3050:{DB_FILE}"
DB_USER = "SYSDBA"
DB_PASS = "masterkey"



@pytest.fixture(scope="module")
def db():
    # Ensure database exists
    if not os.path.exists(DB_FILE):
        try:
            con = fdb.create_database(dsn=DSN, user=DB_USER, password=DB_PASS)
            con.close()
        except Exception as e:
            pytest.skip(f"Cannot create Firebird database: {e}")
    else:
        try:
            con = fdb.connect(dsn=DSN, user=DB_USER, password=DB_PASS)
            con.close()
        except Exception as e:
            pytest.skip(f"Cannot connect to Firebird database: {e}")

    # Now connect via Tina4 Database wrapper (must use fdb:)
    db = Database(f"fdb:{DSN}", DB_USER, DB_PASS)

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


