#  test_Request.py — Unit Tests for Request Global State

This test module validates the default state, mutability, and global sharing of request-related variables in the `tina4_python.Request` module.

---

##  Test Scope

These tests ensure:
- Request globals (e.g. `params`, `headers`, `body`) have correct default values.
- Globals can be safely mutated, shared, and reset.
- All request attributes maintain their expected types and values throughout runtime.

---

## What’s Being Tested?

| Test Case | Purpose |
|-----------|---------|
| `test_req_001_default_values` | Verifies that all request-related global variables are initialized to safe defaults (`None`, `{}` etc.). |
| `test_req_002_mutate_and_reset_request_globals` | Confirms that request attributes are mutable and changes persist until manually reset. |
| `test_req_003_global_state_is_shared` | Simulates real-world behavior where multiple parts of an app access and modify shared request state. |
| `test_req_004_type_integrity` | Ensures that dictionary-type globals maintain their type even after use or mutation. |

---

## Key Globals in `tina4_python.Request`

| Variable | Description |
|----------|-------------|
| `request` | Raw request object. |
| `body` | Parsed request body (usually JSON). |
| `params` | URL or query parameters. |
| `headers` | HTTP headers. |
| `cookies` | Cookie data. |
| `url` | Request URL path. |
| `session` | Session data (dict-like). |
| `files` | Uploaded file data. |
| `raw_request`, `raw_data`, `raw_content` | Low-level request contents. |
| `transport`, `asgi_response` | Transport protocol info and ASGI response object (if any). |

---

##  How to Run

```bash
pytest tina4_python/tests/unit/request/test_Request.py
```