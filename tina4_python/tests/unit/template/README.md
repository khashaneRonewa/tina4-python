#  Template Module Tests

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)  
![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen)  
![Coverage](https://img.shields.io/badge/coverage-100%25-success)

##  Test Suite Overview
This test suite validates the functionality of the `Template.py` module in `tina4_python`, ensuring reliable Twig template rendering, debug utilities, and special type conversions.

It covers:

- Twig environment initialization
- Debug output (`dump`, `production_dump`)
- CSRF/form token generation
- Special type conversion for serialization
- Rendering templates from both file and string
- Error handling during rendering

---

##  Test Case Matrix

###  Positive Test Cases

| ID           | Test Method                                    | Description                                                     | Input                                                        | Expected Output                                                      |
|--------------|------------------------------------------------|-----------------------------------------------------------------|--------------------------------------------------------------|------------------------------------------------------------------------|
| TEMPLATE-001 | `test_init_twig_creates_environment`           | Initialize Twig environment and reuse instance                  | Temporary path to templates                                  | `Template.twig` set, contains `RANDOM` and `formToken` globals        |
| TEMPLATE-002 | `test_production_dump_and_dump`                 | Dump Python objects for debugging in dev mode                   | Dict, `date`, `datetime`, `Session`                          | Returns HTML string with pretty-printed JSON and converted types      |
| TEMPLATE-003 | `test_get_form_token_and_input`                 | Generate CSRF form token and hidden input                       | Form name                                                    | Token string from `tina4_auth.get_token`, HTML input contains token   |
| TEMPLATE-004 | `test_convert_special_types`                    | Convert `date` and `datetime` objects to ISO strings            | Dict with date/datetime, list of dates                       | Converted dict with ISO 8601 strings                                 |
| TEMPLATE-005 | `test_render_twig_template_from_string`         | Render a template from a raw string if file template not found  | String template, context dict                                | Rendered string returned                                              |
| TEMPLATE-006 | `test_render_twig_template_error`               | Handle template rendering errors gracefully                     | Invalid template path or exception thrown                     | Error message string containing exception text                       |
| TEMPLATE-007 | `test_render_calls_render_twig_template`        | Ensure `Template.render` delegates to `render_twig_template`    | Template name string                                          | `"OK"` returned from patched method                                   |

---

###  Negative / Edge Test Cases

| ID           | Test Method                                    | Description                                                     | Input                                                        | Expected Output                                                      |
|--------------|------------------------------------------------|-----------------------------------------------------------------|--------------------------------------------------------------|------------------------------------------------------------------------|
| TEMPLATE-008 | `test_production_dump_and_dump` *(production mode)* | `production_dump` hides output in production mode               | Any object                                                   | Empty string                                                          |
| TEMPLATE-009 | `test_render_twig_template_error`               | Invalid template file causes exception                          | Nonexistent template name                                    | Error message returned in rendered output                             |
| TEMPLATE-010 | `test_convert_special_types` *(non-serializable)* | Non-date/datetime input remains unchanged                       | String `"x"`                                                  | `"x"` returned                                                         |

---

##  How It Works
- **Fixtures**  
  `setup_env` sets `TINA4_DEBUG_LEVEL=ALL` before each test and clears any existing `Template.twig` instance.
- **Twig Environment Tests**  
  Verifies singleton behavior and pre-loaded globals (`RANDOM`, `formToken`).
- **Dump Utilities**  
  Checks both production-safe dump (`production_dump`) and rich debug dump (`dump`) with date/time conversions.
- **Token Handling**  
  Uses `MagicMock` to simulate `tina4_auth.get_token` for predictable CSRF token results.
- **Rendering Logic**  
  Tests both the happy path (template found or rendered from string) and error path (exception during rendering).
