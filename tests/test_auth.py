import pytest
from flask_login import current_user

from ziho.auth.actions import get_user_by_username


def test_register(client, app):
    # test for template errors
    assert client.get("/auth/register").status_code == 200

    resp = client.post(
        "/auth/register",
        data={
            "username": "test",
            "email": "test@test.com",
            "password": "test",
            "password2": "test",
        },
    )

    assert resp.status_code == 302
    assert resp.headers["Location"] == "/auth/login"

    with app.app_context():
        user = get_user_by_username("test")
        assert user is not None


@pytest.mark.parametrize(
    ("username", "email", "password", "password2", "message"),
    (
        ("", "", "", "", b"This field is required"),
        ("test", "", "", "", b"This field is required"),
        ("test", "test", "pass", "pass", b"Invalid email address."),
        ("test", "test@test.com", "pass", "pa", b"Field must be equal to password"),
    ),
)
def test_register_validate_input(client, username, email, password, password2, message):
    resp = client.post(
        "/auth/register",
        data={
            "username": username,
            "password": password,
            "email": email,
            "password2": password2,
        },
    )
    assert message in resp.data


def test_register_duplicate_user(client):
    user = {
        "username": "yumi",
        "email": "yumi@email.com",
        "password": "pass",
        "password2": "pass",
    }
    resp = client.post(
        "/auth/register",
        data=user,
    )

    assert b"Please use a different username." in resp.data
    assert b"Please use a different email address." in resp.data


def test_login(client):
    # test template error
    assert client.get("/auth/login").status_code == 200

    user = {
        "username": "yumi",
        "password": "pass",
    }
    resp = client.post("/auth/login", data=user)
    assert resp.headers["Location"] == "/home"

    with client:
        client.get("/home")
        assert current_user.username == user["username"]


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "pass", b"Invalid username or password"),
        ("yumi", "a", b"Invalid username or password"),
    ),
)
def test_login_validate_input(client, username, password, message):
    resp = client.post(
        "/auth/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )
    assert message in resp.data


def test_logout(client, auth):
    resp = client.get("/auth/logout")
    assert resp.status_code == 302
    assert resp.headers["Location"] == "/home"

    auth.login()
    with client:
        resp = client.get("/auth/logout")
        assert resp.status_code == 302
        assert resp.headers["Location"] == "/home"

