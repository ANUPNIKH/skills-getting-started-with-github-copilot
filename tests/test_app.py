import pytest


def test_get_activities(client):
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # Basic smoke checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister(client):
    activity = "Chess Club"
    email = "teststudent@example.com"

    # Ensure email not already present
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]

    # Signup
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert f"Signed up {email}" in res.json()["message"]

    # Verify present
    res = client.get("/activities")
    assert email in res.json()[activity]["participants"]

    # Duplicate signup should be rejected
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 400

    # Unregister
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert f"Unregistered {email}" in res.json()["message"]

    # Verify removal
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]
