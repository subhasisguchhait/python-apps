import pytest
import uuid

# @pytest.mark.asyncio
# async def test_create_dataset(client):
#     response = await client.post(
#         "/api/v1/datasets/create",
#         json={
#             "name": "test_data",
#             "source": "s3://test",
#             "format": "csv",
#             "owner": "test"
#         }
#     )
#     assert response.status_code == 401  # auth required
#     print(response.json())



async def get_token(client):
    username = f"test_{uuid.uuid4().hex[:8]}"
    await client.post("/api/v1/auth/register", json={
        "username": username,
        "password": "test123"
    })
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": "test123"}  # or json=...
    )
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_authenticated_dataset_create(client):
    token = await get_token(client)
    print("TOKEN:", token)
    response = await client.post(
        "/api/v1/datasets/create",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"secure_data_{uuid.uuid4().hex[:8]}",
            "source": "db",
            "format": "json",
            "owner": "test"
        }
    )
    assert response.status_code == 201