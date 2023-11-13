from urllib.parse import urlparse

import pytest


@pytest.mark.parametrize("path", ("/home", "/user/yumi"))
def test_login_required(client, path):
    resp = client.get(path)
    assert resp.status_code == 302
    assert urlparse(resp.headers["Location"]).path == "/auth/login"


def test_user_profile(client, auth):
    auth.login()

    with client:
        resp = client.get("/user/yumi")
        assert resp.status_code == 200


def test_home(client, auth):
    auth.login()

    with client:
        resp = client.get("/home")
        assert resp.status_code == 200


def test_create_deck(client, auth):
    resp = client.post(
        "/create_deck",
        data={
            "name": "Deck Test 1",
        },
    )

    assert resp.status_code == 302
    auth.login()
    with client:
        resp = client.post(
            "/create_deck",
            data={
                "name": "Deck Test 1",
            },
        )
        assert resp.status_code == 200


def test_create_card(client, auth):
    resp = client.post(
        "/create_card",
        data={
            "name": "Deck Test 1",
        },
    )

    assert resp.status_code == 302
    auth.login()
    with client:
        resp = client.post(
            "/create_card",
            data={
                "deck": 1,
                "front": " Test Card Front 1",
                "back": "Test Card Back 2",
            },
        )
        assert resp.status_code == 200


def test_get_card(client, auth):
    resp = client.post("/get-cards", data={"deck_id": 1})

    # redirected to login page
    assert resp.status_code == 302

    auth.login()
    with client:
        resp = client.post("/get-cards", data={"deck_id": 1})

        assert resp.status_code == 200
        assert resp.json["status"] == True

        resp = client.post("/get-cards", data={"deck_id": 100})

        assert resp.json["status"] == False


def test_save_card(client, auth):
    auth.login()
    with client:
        resp = client.post("/get-cards", data={"deck_id": 1})
        assert resp.json["status"] == True

        card = resp.json["result"][0]
        card["card_info"]["scheduled_days"] = 6
        resp = client.post("/save-card", data=card)

        assert resp.status_code == 200
