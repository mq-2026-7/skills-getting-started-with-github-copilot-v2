from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    activity = activities_response.json()[activity_name]
    assert email not in activity["participants"]


def test_unregister_participant_returns_404_for_unknown_activity():
    response = client.delete("/activities/Unknown Activity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
