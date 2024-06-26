from datetime import datetime
from urllib.parse import urlparse

from flask_login import current_user

from tests.lib.base import ZihoTest
from ziho.core.forms import DATETIME_FORMAT
from ziho.profile.handlers import get_decks_by_user


class TestHome(ZihoTest):
    def test_home_without_login(self, client):
        resp = client.get("/home")
        assert resp.status_code == 302
        assert urlparse(resp.headers["Location"]).path == "/auth/login"

    def test_home_template(self, client, app, auth):
        adolin = self.example_user(app, "adolin")
        auth.login(adolin)
        resp = client.get("/home")
        assert resp.status_code == 200

        html = resp.get_data(as_text=True)

        assert 'href="/auth/logout"' in html
        assert 'href="/home"' in html
        assert 'href="/view-deck"' in html
        assert f'href="/profile/{adolin["username"]}"' in html

        # deck form
        assert 'action="/create-deck"' in html
        assert 'name="deck_name"' in html

        # card form
        assert 'action="/add-card"' in html
        assert 'name="deck_id"' in html
        assert 'name="front"' in html
        assert 'name="back"' in html
        assert 'name="card_image"' in html

        assert 'action="/delete-deck"' in html

    def test_create_deck(self, client, app, auth):
        szeth = self.example_user(app, "szeth")
        deck = self.get_deck()

        resp = client.post("/create-deck", data=deck)
        assert resp.status_code == 302

        with client:

            auth.login(szeth)
            resp = client.post("/create-deck", data=deck, follow_redirects=True)

            assert resp.status_code == 200
            assert "message" in resp.json
            assert "New deck created" in resp.json["message"]

            with app.app_context():
                user_deck = get_decks_by_user(current_user.id)
                assert deck["deck_name"] == user_deck[0].name

                user_deck_tags = [tag.name for tag in user_deck[0].tags]

                assert set(deck["tag_list"]) == set(user_deck_tags)

    def test_add_card(self, client, app, auth):
        moash = self.example_user(app, "szeth")

        with client:
            auth.login(moash)
            deck = self.get_posted_deck(app)
            card = self.get_card(deck["id"], image=True)
            resp = client.post("/add-card", data=card)
            assert resp.status_code == 200
            assert "message" in resp.json
            assert "Card added." in resp.json["message"]
            assert "success_template" in resp.json["result"]

    def test_add_card_validate_input(self, client, app, auth):
        szeth = self.example_user(app, "szeth")

        auth.login(szeth)

        resp = client.post("/add-card", data={})
        assert resp.status_code == 406
        assert "message" in resp.json
        assert "message" in resp.json["message"]

        json_resp = resp.json["message"]
        assert "Invalid form." in json_resp["message"]
        assert "error_template" in json_resp["result"]
        assert "Not a valid choice" in json_resp["result"]["error_template"]
        assert "This field is required" in json_resp["result"]["error_template"]

    def test_add_card_validate_wrong_image_extension(self, client, app, auth):
        szeth = self.example_user(app, "szeth")

        with client:
            auth.login(szeth)
            deck = self.get_posted_deck(app)
            card = self.get_card(deck["id"], image=True, valid_ext=False)

            resp = client.post("/add-card", data=card)
            assert resp.status_code == 406
            json_resp = resp.json["message"]
            assert (
                "Image extensions which are allowed: jpg, jpe, jpeg, png, gif, svg, bmp, webp"
                in json_resp["result"]["error_template"]
            )

    def test_get_card_validate_input(self, client, app, auth):
        dalinar = self.example_user(app, "dalinar")

        resp = client.post("/get-cards", data={"deck_id": 1}, follow_redirects=True)
        assert resp.status_code == 200

        auth.login(dalinar)
        resp = client.post("/get-cards", data={"deck_id": 1})

        assert resp.status_code == 406
        assert "message" in resp.json
        assert "Invalid form data." in resp.json["message"]

    def test_get_card(self, client, app, auth):
        dalinar = self.example_user(app, "dalinar")

        with client:
            auth.login(dalinar)
            card = self.get_posted_card(app, image=True)
            payload = {"deck_id": card["deck_id"]}

            resp = client.post("/get-cards", data=payload, follow_redirects=True)
            assert resp.status_code == 200

            assert resp.json["message"] is None
            assert "result" in resp.json
            assert "card" in resp.json["result"][0]

            card_item = resp.json["result"][0]["card"]
            assert card["card_id"] == card_item["card_id"]
            assert card["front"] in card_item["front"]
            assert card["back"] in card_item["back"]

    def test_update_card_info(self, client, app, auth):
        dalinar = self.example_user(app, "dalinar")

        with client:
            auth.login(dalinar)
            card = self.get_posted_card(app)
            payload = {"deck_id": card["deck_id"]}
            resp = client.post("/get-cards", data=payload, follow_redirects=True)

            assert resp.status_code == 200

            card_info = resp.json["result"][0]["card_info"]

            card_info |= {"card_id": card["card_id"], "deck_id": card["deck_id"]}
            card_info["due"] = datetime.strptime(
                card_info["due"], "%a, %d %b %Y %H:%M:%S %Z"
            ).strftime(DATETIME_FORMAT + "Z")
            card_info["last_review"] = datetime.strptime(
                card_info["last_review"], "%a, %d %b %Y %H:%M:%S %Z"
            ).strftime(DATETIME_FORMAT + "Z")
            card_info["scheduled_days"] = 6
            resp = client.post(
                "/update-card-info", data=card_info, follow_redirects=True
            )
            assert resp.status_code == 200

    def test_update_card_info_validate(self, client, app, auth):
        dalinar = self.example_user(app, "dalinar")

        with client:
            auth.login(dalinar)
            card = self.get_posted_card(app)
            payload = {"deck_id": card["deck_id"]}
            resp = client.post("/get-cards", data=payload, follow_redirects=True)

            assert resp.status_code == 200

            card_info = resp.json["result"][0]["card_info"]

            resp = client.post(
                "/update-card-info", data=card_info, follow_redirects=True
            )

            assert resp.status_code == 406
            assert "message" in resp.json
            assert "Invalid form data." in resp.json["message"]

    def test_delete_deck(self, client, app, auth):
        tarav = self.example_user(app, "tarav")

        with client:
            auth.login(tarav)
            deck = self.get_posted_deck(app)

            resp = client.post(
                "/delete-deck", data={"deck_id": deck["id"]}, follow_redirects=True
            )
            assert resp.status_code == 200

            with app.app_context():
                decks = get_decks_by_user(current_user.id)
                assert len(decks) is 0
