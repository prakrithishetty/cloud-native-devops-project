import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import app


def test_get_users():
    client = app.test_client()

    response = client.get("/api/users")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_deployments():
    client = app.test_client()

    response = client.get("/api/deployments")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_create_user():
    client = app.test_client()

    response = client.post(
        "/api/users",
        json={
            "name": "Test User",
            "role": "Tester"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Test User"
    assert data["role"] == "Tester"


def test_create_deployment():
    client = app.test_client()

    response = client.post(
        "/api/deployments",
        json={
            "version": "v2.0.0",
            "status": "SUCCESS",
            "environment": "Testing"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["version"] == "v2.0.0"
    assert data["status"] == "SUCCESS"