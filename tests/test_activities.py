from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_json():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect at least one known activity from initial dataset
    assert "Basketball" in data


def test_signup_and_unregister_flow():
    test_activity = "Basketball"
    test_email = "test.student@mergington.edu"

    # Ensure email not present initially
    if test_email in activities[test_activity]["participants"]:
        activities[test_activity]["participants"].remove(test_email)

    # Signup
    resp = client.post(f"/activities/{test_activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {test_email} for {test_activity}"
    assert test_email in activities[test_activity]["participants"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{test_activity}/signup?email={test_email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_un = client.post(f"/activities/{test_activity}/unregister?email={test_email}")
    assert resp_un.status_code == 200
    assert resp_un.json()["message"] == f"Unregistered {test_email} from {test_activity}"
    assert test_email not in activities[test_activity]["participants"]

    # Unregistering again should fail
    resp_un2 = client.post(f"/activities/{test_activity}/unregister?email={test_email}")
    assert resp_un2.status_code == 400
