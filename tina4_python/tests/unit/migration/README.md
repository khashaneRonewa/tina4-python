# Migration Module Tests

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)  
![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen)  
![Coverage](https://img.shields.io/badge/coverage-100%25-success)

##  Test Suite Overview
This test suite validates the functionality of the `Migration.py` module in `tina4_python`.  
It ensures database migrations are applied correctly, failures are recorded, and rollback/error handling works as expected.  

It covers:

- Applying new SQL migrations
- Handling repeated migrations
- Detecting and recording SQL errors
- Partial migration failure handling
- Missing and empty migration folders

---

##  Test Case Matrix

###  Positive Test Cases

| ID              | Test Method                          | Description                                             | Input                                | Expected Output                                                                 |
|-----------------|--------------------------------------|---------------------------------------------------------|--------------------------------------|---------------------------------------------------------------------------------|
| MIGRATION-001   | `test_successful_migration`          | Apply a valid SQL migration                             | Migration file with valid SQL         | Table is created and recorded in `tina4_migration`                              |
| MIGRATION-002   | `test_migration_already_applied`     | Skip migration if already applied                       | Migration file applied twice          | Migration recorded once, no duplicates created                                  |
| MIGRATION-003   | `test_empty_migration_folder`        | Handle empty migrations folder gracefully               | Empty migrations directory            | No errors raised, `tina4_migration` remains empty                               |

---

###  Negative / Edge Test Cases

| ID              | Test Method                          | Description                                             | Input                                | Expected Output                                                                 |
|-----------------|--------------------------------------|---------------------------------------------------------|--------------------------------------|---------------------------------------------------------------------------------|
| MIGRATION-004   | `test_invalid_sql_fails_and_rolls_back` | Handle invalid SQL and record failure                  | Migration file with invalid SQL       | Migration marked as failed, error message stored, raises `SystemExit`            |
| MIGRATION-005   | `test_partial_migration_failure`     | Partial failure should record error, but partial success | Migration file with valid + invalid SQL | One table created, migration recorded as failed, raises `SystemExit`            |
| MIGRATION-006   | `test_missing_migration_folder`      | Handle missing migrations folder                        | Nonexistent folder path               | Raises `FileNotFoundError`                                                       |

---

##  How It Works
- **Fixture Setup (`setup_db`)**  
  - Creates a temporary SQLite database.  
  - Prepares a `migrations` folder for test migration files.  
  - Ensures a clean database environment before each test.  

- **Migration Execution**  
  - `migrate(dba)` applies all `.sql` files in the migrations folder.  
  - Results are logged in the `tina4_migration` table (success/failure).  

- **Error Handling**  
  - Invalid or partially valid migrations raise `SystemExit`.  
  - Failures are still recorded with `passed = 0` and the error message stored.  

- **Folder Handling**  
  - If the migrations folder is missing, a `FileNotFoundError` is raised.  
  - If empty, the migration runs successfully with no changes recorded.  

---

##  Coverage Achieved
- Successful migration  
- Duplicate migrations skipped  
- Invalid SQL rollback handling  
- Partial migration failures logged 
- Missing/empty folder handling 

This ensures robust migration handling across all expected scenarios.  


## Technologies Used
- `pytest` for test running

## How to Run Tests

From the project root, run:

```bash
pytest tests/test_migration.py -v
```
