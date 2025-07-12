# tests/unit/test_security.py
import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

def test_hash_and_verify_password():
    pwd = "My$ecret!"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed)

def test_jwt_encode_decode():
    data = {"sub": "42"}
    token = create_access_token(data)
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "42"
    assert "exp" in payload
