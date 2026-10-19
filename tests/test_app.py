def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_student_can_register_for_activity(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up student@mergington.edu for Chess Club"
    }
    assert "student@mergington.edu" in client.get("/activities").json()["Chess Club"]["participants"]


def test_duplicate_registration_is_rejected(client):
    endpoint = "/activities/Chess Club/signup"
    params = {"email": "student@mergington.edu"}

    assert client.post(endpoint, params=params).status_code == 200
    response = client.post(endpoint, params=params)

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_registering_for_unknown_activity_is_rejected(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_student_can_unregister_from_activity(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity}"
    }
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregistering_unknown_participant_is_rejected(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregistering_from_unknown_activity_is_rejected(client):
    response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
