import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the in-memory DB before each test
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))

def test_get_activities():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    client = TestClient(app)
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in response.json()["message"]

def test_signup_already_registered():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    # Arrange
    client = TestClient(app)
    email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/Nonexistent/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    assert "Removed" in response.json()["message"]

def test_unregister_not_signed_up():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not signed up" in response.json()["detail"]

def test_unregister_activity_not_found():
    # Arrange
    client = TestClient(app)
    email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/Nonexistent/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
