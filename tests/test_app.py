
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == (
        "DevOps Task Tracker API is running"
    )


def test_get_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Review healthcare data"}
    )

    assert response.status_code == 201
    assert response.json["title"] == "Review healthcare data"
    assert response.json["status"] == "To Do"


def test_create_task_without_title(client):
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 400


def test_update_task_status(client):
    response = client.patch(
        "/tasks/1",
        json={"status": "In Progress"}
    )

    assert response.status_code == 200
    assert response.json["status"] == "In Progress"


def test_invalid_task_status(client):
    response = client.patch(
        "/tasks/1",
        json={"status": "Invalid"}
    )

    assert response.status_code == 400
