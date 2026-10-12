import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from app import app


def fake_connection(rows):
    connection = MagicMock()
    cursor = MagicMock()
    cursor.fetchall.return_value = rows
    cursor.fetchone.return_value = (1, "Test User", "Tester")
    connection.cursor.return_value = cursor
    return connection


@patch("app.get_db_connection")
def test_get_users(mock_db):
    mock_db.return_value = fake_connection([
        (1, "Test User", "Tester")
    ])

    response = app.test_client().get("/api/users")

    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "name": "Test User", "role": "Tester"}
    ]


@patch("app.get_db_connection")
def test_get_deployments(mock_db):
    mock_db.return_value = fake_connection([
        (1, "v1.0.0", "Development", "SUCCESS", None)
    ])

    response = app.test_client().get("/api/deployments")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["version"] == "v1.0.0"


@patch("app.get_db_connection")
def test_create_user(mock_db):
    mock_db.return_value = fake_connection([])

    response = app.test_client().post(
        "/api/users",
        json={"name": "Test User", "role": "Tester"}
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1, "name": "Test User", "role": "Tester"
    }


@patch("app.get_db_connection")
def test_create_deployment(mock_db):
    mock_db.return_value = fake_connection([])

    cursor = mock_db.return_value.cursor.return_value
    cursor.fetchone.return_value = (
        1, "v2.0.0", "Testing", "SUCCESS"
    )

    response = app.test_client().post(
        "/api/deployments",
        json={
            "version": "v2.0.0",
            "status": "SUCCESS",
            "environment": "Testing"
        }
    )

    assert response.status_code == 201
    assert response.get_json()["version"] == "v2.0.0"
    assert response.get_json()["status"] == "SUCCESS"
