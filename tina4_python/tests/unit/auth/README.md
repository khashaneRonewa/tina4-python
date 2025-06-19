#  Authentication Module Tests

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-success)

##  Test Suite Overview
Comprehensive unit tests for the `Auth.py` module, covering:

- Password hashing/verification (bcrypt)
- JWT token generation/validation
- Security edge cases
- Error handling scenarios

##  Test Case Matrix

| ID       | Test Method                          | Description                      | Key Assertions                     |
|----------|--------------------------------------|----------------------------------|------------------------------------|
| AUTH-001 | `test_auth_001_hash_password`        | Validates bcrypt hashing         | Correct hash format                |
| AUTH-002 | `test_auth_002_check_correct_password` | Password verification           | Returns True for correct passwords |
| AUTH-003 | `test_auth_003_generate_jwt_token`   | JWT generation                  | Valid token structure              |
| AUTH-004 | `test_auth_004_get_payload_from_token` | Payload extraction             | Data integrity                     |
| AUTH-005 | `test_auth_005_validate_valid_jwt_token` | Token validation              | Returns True for valid tokens      |
| AUTH-006 | `test_auth_006_valid_wrapper_returns_true` | Valid() wrapper            | Consistent with validate()         |
| AUTH-007 | `test_auth_007_check_wrong_password` | Wrong password handling         | Returns False                      |
| AUTH-008 | `test_auth_008_invalid_jwt_token_format` | Malformed token handling    | Proper exception raising           |
| AUTH-009 | `test_auth_009_expired_token`        | Expired token validation        | Returns False                      |
| AUTH-010 | `test_auth_010_tampered_jwt_signature` | Tampered token detection     | Returns False                      |

##  Getting Started

### 1. Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows
```

# Install test dependencies

```bash
pip install pytest pytest-cov pytest-mock bcrypt pyjwt cryptography
```

### 2. Running Tests
Basic run

```bash
pytest tina4_python/tests/unit/auth/test_auth.py
```
Detailed Output

```bash
pytest tina4_python/tests/unit/auth/test_auth.py -v
```
With Coverage Reporting

```bash
# Terminal report
pytest --cov=tina4_python/auth --cov-report=term-missing
```

```bash
# HTML report (opens in browser)
pytest --cov=tina4_python/auth --cov-report=html
open htmlcov/index.html
```
Run Specific Test
```bash
pytest tina4_python/tests/unit/auth/test_auth.py::TestAuth::test_auth_001_hash_password -v
```

### Test Components

```python
@pytest.fixture
def auth(tmp_path):  # Creates fresh Auth instance for each test
    """Provides configured Auth instance with temporary keys"""
    ...

@pytest.fixture 
def valid_token(auth):  # Generates valid JWT token
    """Returns a signed JWT with 1-hour expiry"""
    ...
```

### Mocking Examples

```python
# Testing expired tokens
with patch('jwt.encode', return_value="expired.token.mock"):
    with patch('Auth.Auth.get_payload', return_value=expired_payload):
        assert not auth.validate("expired.token.mock")
```

### Troubleshooting

| Symptom      | Solution                         |
|-------|--------------------------|
| ModuleNotFoundError	 | `Run pip install -r requirements.txt` | 
| JWTDecodeError | `Verify test keys in /secrets/ directory` | 
| Missing API Key| `Set API_KEY=testvalue in .env` | 
| Failing Tests | `Run with -v --tb=long for details` |

#### File Location: `tina4_python/tests/unit/auth/test_auth.py`

#### Last Updated: ('2025-06-18')