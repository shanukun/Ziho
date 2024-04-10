import os

import pytest

from config import TestingConfig
from tests import *
from ziho import create_app

basedir = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def app():
    app = create_app(TestingConfig)

    setup_db(app)

    yield app

    teardown_db(app)


@pytest.fixture(scope="function")
def client(app):
    yield app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, example_user):
        return self._client.post("/auth/login", data=example_user)

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
