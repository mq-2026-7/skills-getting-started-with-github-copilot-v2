from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    activities_response = client.get("/activities")
    activity = activities_response.json()[activity_name]

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activity["participants"]


def test_unregister_participant_returns_404_for_unknown_activity():
    # Arrange
    activity_name = "Unknown Activity"
    email = "test@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
