import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Chess Club" in response.json()["message"]

    # Clean up: remove test user
    client.delete("/activities/Chess Club/unregister", params={"email": "testuser@mergington.edu"})

def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
    # First, sign up a test user
    client.post("/activities/Drama Society/signup", params={"email": "testremove@mergington.edu"})
    response = client.delete("/activities/Drama Society/unregister", params={"email": "testremove@mergington.edu"})
    assert response.status_code == 200
    assert "Unregistered testremove@mergington.edu from Drama Society" in response.json()["message"]

def test_unregister_from_activity_not_registered():
    response = client.delete("/activities/Drama Society/unregister", params={"email": "notregistered@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"

def test_unregister_from_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
