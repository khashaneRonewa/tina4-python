#  test_Router.py — Unit Tests for Routing Logic

This module tests the core routing functionality provided by the `Router` class in the `tina4_python` framework. It verifies how URL paths are matched, cleaned, and mapped to their respective route callbacks.

---

##  Test Scope

These tests ensure:
- Route parameter extraction works as expected.
- Route matching logic correctly identifies valid/invalid routes.
- URL normalization is handled (e.g., removing double slashes).
- Routes are registered correctly with HTTP method and path.
- Path parameters are parsed and stored correctly during route registration.

---

##  What’s Being Tested?

| Test Case | Purpose |
|-----------|---------|
| `test_get_variables_extracts_correct_params` | Extracts path parameters from a dynamic route (e.g., `/user/{id}`). |
| `test_match_returns_true_for_matching_route` | Validates that a URL matches a dynamic route and updates `Router.variables`. |
| `test_match_returns_false_for_non_matching_route` | Ensures non-matching URLs return `False`. |
| `test_clean_url_removes_double_slashes` | Confirms that redundant slashes are removed from URLs. |
| `test_add_route_creates_route_entry` | Verifies that routes are stored in the global route registry with method and path. |
| `test_add_route_with_parameters_parses_params` | Ensures route parameters are parsed and stored during registration. |

---

##  Key Components from `tina4_python.Router`

| Method | Description |
|--------|-------------|
| `Router.get_variables(url, route)` | Extracts dynamic route parameters from the URL. |
| `Router.match(url, route)` | Checks if a given URL matches a defined route and sets variables. |
| `Router.clean_url(url)` | Cleans the URL by removing redundant slashes. |
| `Router.add(method, route, callback)` | Registers a new route with HTTP method and callback. |

---

##  How to Run

```bash
pytest tina4_python/tests/unit/router/test_Router.py
```
## Notes
- The tests manipulate the global tina4_python.tina4_routes dictionary, which stores route metadata. It’s reset between relevant test cases.

- Router.variables is used to hold extracted path parameters during route matching and should be validated after a match() call.

