from src.app import activities


def test_signup_success_adds_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    activity_name = "Programming Class"
    existing_email = activities[activity_name]["participants"][0]

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_success_removes_participant(client):
    activity_name = "Gym Class"
    existing_email = activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": existing_email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {existing_email} from {activity_name}"}
    assert existing_email not in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Club/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    activity_name = "Science Club"
    email = "not-enrolled@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
