#  Middleware Unit Tests - Tina4 Framework

This test suite covers the `MiddleWare` class in the Tina4 Python framework. The `MiddleWare` module is responsible for classifying and executing custom `before_`, `after_`, and general middleware methods on HTTP request/response objects.

---

##  What It Tests

| Test ID        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| MIDDLEWARE-001 | Identifies `before_` methods in a middleware class                          |
| MIDDLEWARE-002 | Identifies `after_` methods in a middleware class                           |
| MIDDLEWARE-003 | Identifies general (non-prefixed) middleware methods                        |
| MIDDLEWARE-004 | Executes all `before_` methods and updates the request                      |
| MIDDLEWARE-005 | Executes all `after_` methods and updates the response                      |
| MIDDLEWARE-006 | Executes all general middleware methods and updates the request/response    |
| MIDDLEWARE-007 | Invokes a middleware method by name (direct method call)                   |
| MIDDLEWARE-008 | Handles empty middleware class gracefully                                   |
| MIDDLEWARE-009 | Raises `AttributeError` on direct call to a non-existent method             |
| MIDDLEWARE-010 | Confirms method names like `beforenoon` are treated as general methods      |

---

##  File Under Test

- [`tina4_python/MiddleWare.py`](../../../../MiddleWare.py)

---

##  Test File Location

- `tina4_python/tests/unit/middleware/test_middleware.py`

---

##  How to Run

From the root of your project:

```bash
pytest tina4_python/tests/unit/middleware/test_middleware.py -v
```
If using PyCharm, right-click the file and select Run 'pytest in test_middleware.py'.

# Test Setup
Each test uses a simple middleware class that mutates a Python dict (request, response) to simulate middleware behavior.

Pytest fixtures initialize shared request/response objects.

Assertions validate classification logic and proper method execution.

# Notes
All middleware method detection is based on name prefixes: before_, after_.

General methods (like handle, transform, etc.) fall under any_methods.



