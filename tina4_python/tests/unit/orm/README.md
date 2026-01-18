#  test_orm.py — Unit Tests for ORM Functionality

This test module validates the Tina4 Python ORM layer by testing how model fields, object mapping, and basic CRUD operations behave in isolation from the database.

---

##  Test Scope

These tests ensure that:
- ORM model classes behave correctly with field defaults, SQL generation, and save/delete functionality.
- The ORM layer can dynamically initialize models from the project folder.
- ORM fields like `IntegerField`, `StringField`, `ForeignKeyField`, etc., generate the correct definitions and mappings.
- SQL is generated properly for table creation and insertion.

---

##  Mock Setup

All tests use Python’s `unittest.mock` to simulate a working database environment:
- `mock_dba`: A shared fixture that mocks Tina4’s database engine behavior, including inserts, updates, selects, and transactions.
- No actual database is needed. These tests are isolated and fast.

---

##  Key Tests Explained

| Test Function | Purpose |
|---------------|---------|
| `test_integer_field_properties` | Verifies basic `IntegerField` properties like primary key, default value, and type casting. |
| `test_string_field_definition` | Checks if `StringField` generates the correct SQL with default values and length constraints. |
| `test_foreign_key_definition` | Confirms that `ForeignKeyField` links correctly to referenced tables. |
| `test_orm_init_and_to_dict` | Ensures ORM models initialize from dictionaries and convert back using `to_dict()`. |
| `test_orm_save_insert` | Tests saving a new record using the ORM interface. |
| `test_orm_delete` | Tests ORM record deletion behavior. |
| `test_orm_select` | Confirms that `.select()` returns mock results with correct formatting and record count. |
| `test_orm_initializer_creates_classes` | Tests auto-loading of ORM classes from the `orm/` directory. |
| `test_create_table_sql_generation` | Validates dynamic SQL generation for table creation. |

---

##  Running the Tests

```bash
pytest tina4_python/tests/unit/orm/test_orm.py
```