from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert payload

    first_activity = next(iter(payload.values()))
    assert set(first_activity.keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }


def test_get_activities_matches_in_memory_store(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == activities
