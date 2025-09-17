#  test_Response.py — Unit Tests for the Response Handling

This module tests the core behavior of the `tina4_python.Response` class and the global response variables used throughout the Tina4 Python framework. It ensures consistent behavior when returning various types of responses (HTML, JSON, redirects, etc.) across the app.

---

##  Test Scope

These tests validate:
- Correct content type resolution based on data type.
- Default and custom HTTP status codes.
- Global response headers and body handling.
- Utility behavior like redirects and global resets.

---

##  What’s Being Tested?

| Test Case | Purpose |
|-----------|---------|
| `test_response_with_string` | Ensures a plain string is returned as HTML with HTTP 200. |
| `test_response_with_dict` | Automatically serializes a dictionary to JSON format. |
| `test_response_with_list` | Automatically serializes a list to JSON format. |
| `test_response_with_bool_true` / `test_response_with_bool_false` | Confirms booleans are stringified as plain text. |
| `test_response_with_module_type` | Handles unexpected types (like `types` module) gracefully with a fallback error response. |
| `test_response_with_custom_http_code_and_headers` | Applies custom status codes and response headers correctly. |
| `test_response_redirect_sets_correct_headers` | Validates redirect logic and required headers. |
| `test_add_header_updates_global_headers` | Ensures headers added via `add_header()` persist in the final response. |

---

##  Key Components from `tina4_python.Response`

| Component | Role |
|----------|------|
| `Response(data, http_code_in=200, headers_in={})` | Constructs a response with auto-detected content type based on `data`. |
| `Response.add_header(key, value)` | Adds global response headers. |
| `Response.redirect(path)` | Returns a redirect response with status code `302` and a `Location` header. |
| Global Vars | `headers`, `content`, `http_code`, and `content_type` are shared across the module and reset before each test. |

---

##  How to Run

```bash
pytest tina4_python/tests/unit/response/test_Response.py
```