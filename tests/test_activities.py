def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert set(activities["Chess Club"]) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }


def test_signup_adds_participant(client):
    email = "student@example.com"

    response = client.post("/activities/Art Studio/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Art Studio"}
    assert email in client.get("/activities").json()["Art Studio"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    email = "michael@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert client.get("/activities").json()["Chess Club"]["participants"].count(email) == 1


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup", params={"email": "student@example.com"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_unregisters_participant(client):
    email = "student@example.com"
    client.post("/activities/Art Studio/signup", params={"email": email})

    response = client.delete(f"/activities/Art Studio/participants/{email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Art Studio"}
    assert email not in client.get("/activities").json()["Art Studio"]["participants"]


def test_delete_rejects_unknown_participant(client):
    response = client.delete(
        "/activities/Art Studio/participants/unknown@example.com"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_delete_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Club/participants/student@example.com"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
