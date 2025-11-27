import pytest
from tests.factories import UserFactory

@pytest.mark.asyncio
async def test_create_user(client):
    payload = {
        "email": "testuser@example.com",
        "password": "password123",
        "role": "Student"
    }
    response = await client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["role"] == payload["role"]

@pytest.mark.asyncio
async def test_get_users(client, db_session):
    user = UserFactory(session=db_session)
    await db_session.commit()
    response = await client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == user.email

@pytest.mark.asyncio
async def test_get_user(client, db_session):
    user = UserFactory(session=db_session)
    await db_session.commit()
    response = await client.get(f"/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email

@pytest.mark.asyncio
async def test_update_user(client, db_session):
    user = UserFactory(session=db_session)
    await db_session.commit()
    payload = {"email": "updated@example.com", "password": "newpass", "role": "Instructor"}
    response = await client.put(f"/users/{user.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["role"] == payload["role"]

@pytest.mark.asyncio
async def test_partial_update_user(client, db_session):
    user = UserFactory(session=db_session)
    await db_session.commit()
    payload = {"email": "partial@example.com"}
    response = await client.patch(f"/users/{user.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]

@pytest.mark.asyncio
async def test_delete_user(client, db_session):
    user = UserFactory(session=db_session)
    await db_session.commit()
    response = await client.delete(f"/users/{user.id}")
    assert response.status_code == 204
    # перевірка, що користувача більше немає
    get_resp = await client.get(f"/users/{user.id}")
    assert get_resp.status_code == 404
