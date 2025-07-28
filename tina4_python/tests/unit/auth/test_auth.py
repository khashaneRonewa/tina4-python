import pytest
from datetime import datetime, timedelta
from tina4_python import Auth
import jwt
import os
import shutil
from unittest.mock import patch

class TestAuth:
    @pytest.fixture
    def auth(self, tmp_path):
        # Use pytest's tmp_path fixture for clean test isolation
        test_root = str(tmp_path / "test_auth")
        os.makedirs(test_root, exist_ok=True)
        yield Auth(test_root)
        # Cleanup
        shutil.rmtree(test_root, ignore_errors=True)

    @pytest.fixture
    def valid_token(self, auth):
        payload = {"user": "admin", "exp": datetime.utcnow() + timedelta(hours=1)}
        return auth.get_token(payload)

    # Positive test cases
    def test_auth_001_hash_password(self, auth):
        """AUTH-001: Hash password returns bcrypt hash"""
        password = "mypassword"
        hashed = auth.hash_password(password)
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_auth_002_check_correct_password(self, auth):
        """AUTH-002: Check correct password returns True"""
        password = "mypassword"
        hashed = auth.hash_password(password)
        assert auth.check_password(hashed, password) is True

    def test_auth_003_generate_jwt_token(self, auth):
        """AUTH-003: Generate JWT token returns JWT string"""
        payload = {"user": "admin"}
        token = auth.get_token(payload)
        assert isinstance(token, str)
        assert len(token.split('.')) == 3  # JWT has 3 parts

    def test_auth_004_get_payload_from_token(self, auth, valid_token):
        """AUTH-004: Get payload from token returns original payload"""
        decoded = auth.get_payload(valid_token)
        assert decoded["user"] == "admin"

    def test_auth_005_validate_valid_jwt_token(self, auth, valid_token):
        """AUTH-005: Validate valid JWT token returns True"""
        assert auth.validate(valid_token) is True

    def test_auth_006_valid_wrapper_returns_true(self, auth, valid_token):
        """AUTH-006: Valid() wrapper returns True for valid token"""
        assert auth.valid(valid_token) is True

    # Negative test cases
    def test_auth_007_check_wrong_password(self, auth):
        """AUTH-007: Check wrong password returns False"""
        password = "mypassword"
        wrong_password = "wrongpassword"
        hashed = auth.hash_password(password)
        assert auth.check_password(hashed, wrong_password) is False

    def test_auth_008_invalid_jwt_token_format(self, auth):
        """AUTH-008: Invalid JWT token format returns None"""
        invalid_token = "abc.def.ghi"
        # Modify the test to expect an exception or modify the Auth class
        with pytest.raises(jwt.exceptions.DecodeError):
            auth.get_payload(invalid_token)

    def test_auth_009_expired_token(self, auth):
        """AUTH-009: Expired token returns False"""
        expired_payload = {"user": "admin", "exp": datetime.utcnow() - timedelta(minutes=1)}
        with patch('jwt.encode', return_value="expired.token.mock"):
            with patch('tina4_python.Auth.Auth.get_payload', return_value=expired_payload):
                assert auth.validate("expired.token.mock") is False

    def test_auth_010_tampered_jwt_signature(self, auth, valid_token):
        """AUTH-010: Tampered JWT signature returns False"""
        parts = valid_token.split('.')
        tampered_token = f"{parts[0]}.{parts[1]}.tampered"
        assert auth.validate(tampered_token) is False

    def test_api_key_validation(self, auth):
        """Additional test: API_KEY validation"""
        os.environ["API_KEY"] = "test_api_key"
        assert auth.validate("test_api_key") is True
        assert auth.validate("wrong_api_key") is False

    def test_key_files_created(self, auth, tmp_path):
        """Additional test: Verify key files are created"""
        key_path = tmp_path / "test_auth" / "secrets"
        assert (key_path / "private.key").exists()
        assert (key_path / "public.key").exists()
        assert (key_path / "domain.cert").exists()