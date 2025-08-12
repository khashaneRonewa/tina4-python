#  Session Module Tests

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-success)

##  Test Suite Overview
Comprehensive unit tests for the `Session.py` module, covering:

- File-based session handling
- Redis-backed session handling
- Session data CRUD operations
- Error handling for invalid keys, missing dependencies, and expired tokens
- Edge cases for storage failures and corrupted session data

---

##  Test Case Matrix

| ID         | Test Method                                         | Description                                                | Input                                        | Expected Output                                                                 |
|------------|----------------------------------------------------|------------------------------------------------------------|----------------------------------------------|---------------------------------------------------------------------------------|
| SESSION-001 | `test_session_001_file_session_initialization`     | File session creation in specified path                    | New `Session` with file handler              | Session file created in target directory                                        |
| SESSION-002 | `test_session_002_session_data_setting`            | Session data storage                                       | `session.set("key", "value")`                | Value stored and persisted                                                       |
| SESSION-003 | `test_session_003_session_data_retrieval`          | Retrieve session value                                     | `session.get("key")` after setting           | Correct value returned                                                           |
| SESSION-004 | `test_session_004_session_data_removal`            | Remove session key                                         | `session.unset("key")`                       | Key removed and `get()` returns `None`                                          |
| SESSION-005 | `test_session_005_session_loading`                 | Load existing session from file                            | Existing session hash                        | Previous session values restored                                                 |
| SESSION-006 | `test_session_006_session_cleanup`                 | Close and delete session                                   | `session.close()`                            | Session file removed and returns `True`                                         |
| SESSION-007 | `test_session_007_redis_session_initialization`    | Redis session creation                                     | `Session(_default_handler="SessionRedisHandler")` | Redis handler initialized                                                        |
| SESSION-008 | `test_session_008_multiple_session_values`         | Store multiple values                                      | Multiple `set()` calls                       | All values stored and retrievable                                                |
| SESSION-009 | `test_session_009_invalid_session_key_access`      | Access non-existent session key                            | `session.get("non-existent")`                | Returns `None`                                                                   |
| SESSION-010 | `test_session_010_missing_redis_dependency`        | Missing Redis library handling                             | Redis handler without `redis` installed      | Error logged, no crash                                                           |
| SESSION-011 | `test_session_011_invalid_session_file_access`     | Handle corrupted session file                              | Load invalid file content                    | New session started, error logged                                                |
| SESSION-012 | `test_session_012_expired_session_token`           | Expired session token handling                             | Expired auth token in file                   | New session started                                                              |
| SESSION-013 | `test_session_013_invalid_storage_path`            | Non-writable session directory                             | Invalid storage path                         | Save fails, error logged                                                         |

---

### Install test dependencies
```bash
pip install pytest pytest-cov pytest-mock redis
```
1. Running Tests
Basic run:

```bash
pytest tina4_python/tests/unit/session/test_session.py
```
Detailed output:

```bash
pytest tina4_python/tests/unit/session/test_session.py -v
```
With coverage reporting:

```bash
# Terminal coverage report
pytest --cov=tina4_python/Session --cov-report=term-missing
```

Run specific test:

```bash
pytest tina4_python/tests/unit/session/test_session.py::test_session_005_session_loading -v
```

# File Location: tina4_python/tests/unit/session/test_session.py