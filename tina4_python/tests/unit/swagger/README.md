#  Swagger Module Tests

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-success)

##  Test Suite Overview
Comprehensive unit tests for the `Swagger.py` module, covering:

- Route metadata annotation (`description`, `summary`, `tags`, `params`, `example`, `secure`)
- Automatic OpenAPI 3.0 JSON generation
- Path parameter parsing
- Default value fallbacks for incomplete metadata
- Handling of invalid or missing annotation inputs

---

##  Test Case Matrix

### Positive Test Cases

| ID          | Test Method                                         | Description                           | Input                                             | Expected Output                                                |
|-------------|-----------------------------------------------------|---------------------------------------|---------------------------------------------------|----------------------------------------------------------------|
| SWAGGER-001 | `test_swagger_001_route_description_annotation`      | Store route description               | `@description("Test endpoint")`                   | Description stored in route metadata                          |
| SWAGGER-002 | `test_swagger_002_route_summary_annotation`          | Store route summary                   | `@summary("Test summary")`                        | Summary stored in route metadata                              |
| SWAGGER-003 | `test_swagger_003_secure_route_annotation`           | Mark route as secure                  | `@secure()`                                       | Secure flag set in route metadata                             |
| SWAGGER-004 | `test_swagger_004_tags_annotation`                   | Assign tags to route                  | `@tags(["test"])`                                 | Tags stored in route metadata                                 |
| SWAGGER-005 | `test_swagger_005_example_annotation`                | Provide example request/response      | `@example({"key": "value"})`                      | Example stored in route metadata                              |
| SWAGGER-006 | `test_swagger_006_parameters_annotation`             | Add route parameters                  | `@params(["param1=default"])`                     | Parameters stored in route metadata                           |
| SWAGGER-007 | `test_swagger_007_path_parameter_extraction`         | Extract parameters from route path    | Route path `"/users/{id}"`                        | Parameter definition for `"id"` generated                     |
| SWAGGER-008 | `test_swagger_008_swagger_json_generation`           | Generate Swagger JSON                  | Multiple annotated routes                         | Valid OpenAPI 3.0 JSON output                                 |
| SWAGGER-009 | `test_swagger_009_metadata_parsing_defaults`         | Parse partial metadata with defaults  | Partial Swagger metadata                          | Default values filled in for missing fields                   |

---

### Negative Test Cases

| ID          | Test Method                                         | Description                           | Input                                             | Expected Output                                                |
|-------------|-----------------------------------------------------|---------------------------------------|---------------------------------------------------|----------------------------------------------------------------|
| SWAGGER-010 | `test_swagger_010_empty_route_metadata`              | Handle route without annotations      | No decorators applied                             | Default values in generated JSON                              |
| SWAGGER-011 | `test_swagger_011_invalid_parameter_format`          | Handle malformed parameter            | `@params(["invalid"])`                            | Parameter parsed with empty default                           |
| SWAGGER-012 | `test_swagger_012_missing_host_information`          | Handle missing Host header            | Request object without `"Host"` header            | Default host used in generated documentation                  |

---

### 1. Running Tests
Basic run:

```bash
pytest tina4_python/tests/unit/swagger/test_swagger.py
```
Detailed output:

```bash
pytest tina4_python/tests/unit/swagger/test_swagger.py -v
```

Run a specific test:

```bash
pytest tina4_python/tests/unit/swagger/test_swagger.py::test_swagger_008_swagger_json_generation -v
```

File Location: tina4_python/tests/unit/swagger/test_swagger.py