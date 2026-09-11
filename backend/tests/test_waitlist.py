"""Tests for the FlexHEP health and waitlist endpoints."""


def test_health_endpoint_with_isolated_client(isolated_client):
    response = isolated_client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_waitlist_signup_persists_email(get_session_client):
    _, client = get_session_client

    response = client.post(
        "/api/v1/waitlist",
        json={"email": "  PT@example.com "},
    )

    assert response.status_code == 201
    assert response.json()["message"] == "You are on the FlexHEP list."


def test_waitlist_signup_rejects_duplicates(get_session_client):
    _, client = get_session_client
    payload = {"email": "hello@example.com"}

    first_response = client.post("/api/v1/waitlist", json=payload)
    second_response = client.post("/api/v1/waitlist", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert "already" in second_response.json()["detail"]


def test_waitlist_signup_validates_email(get_session_client):
    _, client = get_session_client

    response = client.post(
        "/api/v1/waitlist",
        json={"email": "not-an-email"},
    )

    assert response.status_code == 422
