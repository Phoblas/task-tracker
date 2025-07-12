# tests/integration/test_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login_and_me(client: AsyncClient):
    # 1) регистрируем
    resp = await client.post("/auth/register", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "pass123"
    })
    assert resp.status_code == 201

    # 2) логинимся
    resp = await client.post("/auth/login", json={
        "email": "bob@example.com",
        "password": "pass123"
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    # 3) /auth/me
    resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    data = resp.json()
    assert data["email"] == "bob@example.com"
    assert data["username"] == "bob"
