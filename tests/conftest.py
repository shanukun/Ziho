import os

import pytest

from config import TestingConfig
from ziho import create_app, db
from ziho.auth.actions import create_user
from ziho.main.actions import create_deck

basedir = os.path.abspath(os.path.dirname(__file__))


test_user_yumi = {
    "username": "yumi",
    "email": "yumi@email.com",
    "password": "pass",
}

test_deck = {"name": "Test Deck 1"}


@pytest.fixture()
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()
        user_id = create_user(
            test_user_yumi["username"],
            test_user_yumi["email"],
            test_user_yumi["password"],
        )
        create_deck(test_deck["name"], user_id)

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(
        self, username=test_user_yumi["username"], password=test_user_yumi["password"]
    ):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
