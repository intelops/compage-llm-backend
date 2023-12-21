from tests.config import client

def test_create_token():
    response = client.post(
        "/api/create-token", json={"api_key": "string", "username": "string"}
    )
    assert response.status_code == 400
