#  Database Module Tests

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-success)

##  Test Suite Overview

Comprehensive unit tests for the `Database.py` module, covering:

- SQLite and MySQL database connections
- Table creation and existence checking
- Insert, update, delete operations (with edge cases)
- Query execution (`fetch`, `fetch_one`, `execute`, `execute_many`)
- Transaction control (`start_transaction`, `commit`, `rollback`)
- Utility methods like `get_next_id`, `check_connected`
- Error handling for invalid SQL, connection strings, and data types

---

##  Test Case Matrix

| ID        | Test Method                                 | Description                             | Key Assertions                          |
|-----------|---------------------------------------------|-----------------------------------------|-----------------------------------------|
| DBMAIN-001 | `test_DBMAIN_001_sqlite_connection`         | SQLite driver and connection init       | Engine type, dba instance                |
| DBMAIN-002 | `test_DBMAIN_002_mysql_connection`          | MySQL connection handling               | Driver load and connection success       |
| DBMAIN-003 | `test_DBMAIN_003_table_exists_true`         | Detects existing table                  | Returns `True`                          |
| DBMAIN-004 | `test_DBMAIN_004_fetch_records`             | Multi-record SQL fetch                  | Result count, record structure          |
| DBMAIN-005 | `test_DBMAIN_005_fetch_one_record`          | Single record fetch                     | Exact value match                       |
| DBMAIN-006 | `test_DBMAIN_006_execute_insert`            | Direct SQL insert execution             | No errors on insert                     |
| DBMAIN-007 | `test_DBMAIN_007_execute_update`            | Direct SQL update                       | Update succeeds                         |
| DBMAIN-008 | `test_DBMAIN_008_execute_delete`            | Direct SQL delete                       | Deletion succeeds                       |
| DBMAIN-009 | `test_DBMAIN_009_transaction_commit`        | Commit functionality                    | Record persists                         |
| DBMAIN-010 | `test_DBMAIN_010_data_type_conversion_datetime` | Date/time value conversion          | ISO string or epoch detected            |
| DBMAIN-011 | `test_DBMAIN_011_insert_method`             | Uses `.insert()`                        | Record inserted correctly               |
| DBMAIN-012 | `test_DBMAIN_012_update_method`             | Uses `.update()`                        | Record modified correctly               |
| DBMAIN-013 | `test_DBMAIN_013_delete_method`             | Uses `.delete()`                        | Record deleted correctly                |
| DBMAIN-014 | `test_DBMAIN_014_get_next_id`               | Gets next ID from existing table        | Next ID = Max + 1                       |
| DBMAIN-015 | `test_DBMAIN_015_invalid_connection_string` | Invalid driver string handling          | Exits with error                        |
| DBMAIN-016 | `test_DBMAIN_016_table_exists_false`        | Non-existent table check                | Returns `False`                         |
| DBMAIN-017 | `test_DBMAIN_017_fetch_invalid_sql`         | Malformed SQL for fetch                 | Returns error                           |
| DBMAIN-018 | `test_DBMAIN_018_execute_invalid_sql`       | Malformed SQL for execute               | Returns error                           |
| DBMAIN-019 | `test_DBMAIN_019_transaction_rollback`      | Rollback after insert                   | Record does not persist                 |
| DBMAIN-020 | `test_DBMAIN_020_fetch_one_empty_result`    | Fetch one when no record exists         | Returns `None`                          |
| DBMAIN-021 | `test_DBMAIN_021_insert_invalid_data`       | Invalid input for `.insert()`           | Returns `False` or `None`               |
| DBMAIN-022 | `test_DBMAIN_022_update_non_existent`       | Update non-existent record              | Returns `False` or `True`               |
| DBMAIN-023 | `test_DBMAIN_023_delete_non_existent`       | Delete non-existent record              | Returns `False` or `True`               |
| DBMAIN-024 | `test_DBMAIN_024_get_next_id_empty_table`   | Get next ID from empty table            | Returns `1`                             |
| DBMAIN-025 | `test_DBMAIN_025_check_connected_on_closed_connection` | Ping closed DB safely        | No exception thrown                     |

---

##  Getting Started

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.\.venv\Scripts\activate       # Windows
```

### 2. Install Dependencies

```bash
pip install pytest mysql-connector-python
```
Additional drivers (e.g., psycopg2, pymssql) can be added if extending test coverage.

### 2. Running Tests

Basic run
```bash
pytest tina4_python/tests/units/database/test_database.py
```
Verbose Output
```bash
pytest tina4_python/tests/units/database/test_database.py -v
```

With Coverage Report
```bash
# Terminal output
pytest --cov=tina4_python/Database --cov-report=term-missing
```
```bash
# HTML report
pytest --cov=tina4_python/Database --cov-report=html
open htmlcov/index.html
```

Run a Specific Test
```bash
pytest tina4_python/tests/units/database/test_database.py::test_DBMAIN_010_data_type_conversion_datetime -v
```

Optional: MySQL Docker Setup (for DBMAIN-002)
```bash
pytest tina4_python/tests/units/database/test_database.py::test_DBMAIN_010_data_type_conversion_datetime -v
```
- Host: `localhost`
- Port: `33066`
- User: `root`
- Password: `secret`
- Database: `test`

The test will skip if the connection fails.

### Fixtures Overview

```python
@pytest.fixture(scope="module")
def db():
    return Database("sqlite3:test_db_unit.db")  # Default test DB
```

### Troubleshooting

| Symptom      | Solution                                    |
|-------|---------------------------------------------|
| ModuleNotFoundError	 | Run `pip install -r requirements.txt`       | 
| `SystemExit` on MySQL test | Ensure Docker is running MySQL on port 33066 | 
| `NoneType` error on record| Confirm table and data setup before fetch             | 
| SQLite adapter warnings| Ignore — adapters are registered dynamically         |

#### File Location: `tina4_python/tests/units/database/test_database.py`

#### Last Updated: ('2025-06-20')