import pytest
from flask_login import current_user

from tests.lib.base import ZihoTest
from ziho.auth.handlers import get_user_by_username


class TestUserRegistration(ZihoTest):
    def test_register_template(self, client):
        resp = client.get("/auth/register")
        assert resp.status_code == 200

        html = resp.get_data(as_text=True)

        assert 'name="username"' in html
        assert 'name="email"' in html
        assert 'name="password"' in html
        assert 'name="password2"' in html
        assert 'name="submit"' in html

    def test_register(self, client, app):
        vasher = self.nonreg_user("vasher")
        resp = client.post("/auth/register", data=vasher)

        with app.app_context():
            user = get_user_by_username(vasher["username"])
            assert user is not None

        assert resp.status_code == 302
        assert resp.headers["Location"] == "/auth/login"

    @pytest.mark.parametrize(
        ("username", "email", "password", "password2", "message"),
        (
            ("", "", "", "", b"This field is required"),
            ("test", "", "", "", b"This field is required"),
            ("test", "test", "pass", "pass", b"Invalid email address."),
            ("test", "test@test.com", "pass", "pa", b"Field must be equal to password"),
        ),
    )
    def test_register_validate_input(
        self, client, username, email, password, password2, message
    ):
        resp = client.post(
            "/auth/register",
            data={
                "username": username,
                "email": email,
                "password": password,
                "password2": password2,
            },
        )
        assert message in resp.data

    def test_register_duplicate_user(self, client, app):
        szeth = self.example_user(app, "szeth", all_info=True)

        resp = client.post("/auth/register", data=szeth)

        assert b"Please use a different username." in resp.data
        assert b"Please use a different email address." in resp.data


class TestUserLogin(ZihoTest):
    def test_login_template(self, client):
        response = client.get("/auth/login")
        assert response.status_code == 200

        html = response.get_data(as_text=True)

        assert 'name="username"' in html
        assert 'name="password"' in html
        assert 'name="submit"' in html

    def test_login(self, client, app):
        kaladin = self.example_user(app, "kaladin")
        resp = client.post("/auth/login", data=kaladin)
        assert resp.headers["Location"] == "/home"

        with client:
            client.get("/home")
            assert current_user.username == kaladin["username"]

    @pytest.mark.parametrize(
        ("username", "password", "message"),
        (
            ("a", "pass", b"Invalid username or password"),
            ("navani", "a", b"Invalid username or password"),
        ),
    )
    def test_login_validate_input(self, client, app, username, password, message):
        self.example_user(app, "navani")

        resp = client.post(
            "/auth/login",
            data={"username": username, "password": password},
            follow_redirects=True,
        )
        assert message in resp.data

    def test_login_next(self, client, app):
        shallan = self.example_user(app, "shallan")
        resp = client.post("/auth/login?next=/view-deck", data=shallan)
        assert resp.status_code == 302
        assert resp.headers["Location"] == "/view-deck"


class TestLogout(ZihoTest):
    def test_logout(self, client, app, auth):
        resp = client.get("/auth/logout")
        assert resp.status_code == 302
        assert resp.headers["Location"] == "/home"

        dalinar = self.example_user(app, "dalinar")

        with client:
            auth.login(dalinar)
            assert current_user.username == "dalinar"
            resp = client.get("/auth/logout")
            assert resp.status_code == 302
            assert resp.headers["Location"] == "/home"
