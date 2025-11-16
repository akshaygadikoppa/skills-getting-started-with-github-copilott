from src import app as app_module


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activities present
    assert "Chess Club" in data


def test_signup_and_unregister(client):
    activity = "Chess Club"
    email = "pytest-user@example.com"

    # Ensure email not currently in participants
    before = client.get("/activities").json()[activity]["participants"]
    assert email not in before

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # Confirm participant present
    after = client.get("/activities").json()[activity]["participants"]
    assert email in after

    # Unregister
    r2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r2.status_code == 200
    assert "Unregistered" in r2.json().get("message", "")

    # Confirm removed
    final = client.get("/activities").json()[activity]["participants"]
    assert email not in final


def test_signup_already_signed_up_returns_400(client):
    activity = "Chess Club"
    # Use an existing participant from the seed data
    existing = app_module.activities[activity]["participants"][0]

    r = client.post(f"/activities/{activity}/signup?email={existing}")
    assert r.status_code == 400


def test_unregister_nonexistent_returns_404(client):
    activity = "Chess Club"
    email = "not-registered@example.com"

    r = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r.status_code == 404
