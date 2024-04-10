from urllib.parse import urlparse

from tests.lib.base import ZihoTest


class TestDeckView(ZihoTest):
    def test_deckview_without_login(self, client):
        resp = client.get("/view-deck")
        assert resp.status_code == 302
        assert urlparse(resp.headers["Location"]).path == "/auth/login"

    def test_deckview_emtpy_template(self, client, app, auth):
        adolin = self.example_user(app, "adolin")
        auth.login(adolin)

        resp = client.get("/view-deck")
        assert resp.status_code == 200

        html = resp.get_data(as_text=True)
        assert "Empty" in html

    def test_deckview_invalid_deck(self, client, app, auth):
        shallan = self.example_user(app, "shallan")

        with client:
            auth.login(shallan)
            self.get_posted_card(app)
            resp = client.get("/view-deck/" + "99")
            assert resp.status_code == 404

    def test_deckview(self, client, app, auth):
        szeth = self.example_user(app, "szeth")

        with client:
            auth.login(szeth)
            card = self.get_posted_card(app)
            resp = client.get("/view-deck")
            assert resp.status_code == 200

            html = resp.get_data(as_text=True)
            assert 'action="/update-card"' in html
            assert 'name="deck_id"' in html
            assert 'name="front"' in html
            assert 'name="back"' in html
            assert 'name="card_image"' in html

            assert 'action="/delete-card"' in html

            resp = client.get("/view-deck/" + str(card["deck_id"]))
            assert resp.status_code == 200

            html = resp.get_data(as_text=True)

            assert card["front"] in html
            assert card["back"] in html

    def test_update_card(self, client, app, auth):
        navani = self.example_user(app, "navani")

        with client:
            auth.login(navani)
            card = self.get_posted_card(app, image=True)
            card["front"] = "test front"
            card["card_image"] = None
            resp = client.post("/update-card", data=card)
            assert resp.status_code == 200
            assert "message" in resp.json
            assert "Card updated." in resp.json["message"]
            assert "success_template" in resp.json["result"]

    def test_update_card_validate_input(self, client, app, auth):
        tarav = self.example_user(app, "tarav")

        with client:
            auth.login(tarav)

            resp = client.post("/update-card", data={})
            assert resp.status_code == 406
            assert "message" in resp.json
            assert "message" in resp.json["message"]

            json_resp = resp.json["message"]
            assert "Invalid form." in json_resp["message"]
            assert "error_template" in json_resp["result"]
            assert "This field is required" in json_resp["result"]["error_template"]

    def test_update_card_validate_wrong_image_extension(self, client, app, auth):
        szeth = self.example_user(app, "szeth")

        with client:
            auth.login(szeth)
            deck = self.get_posted_deck(app)
            card = self.get_card(deck["id"], image=True, valid_ext=False)

            resp = client.post("/update-card", data=card)
            assert resp.status_code == 406
            json_resp = resp.json["message"]
            assert (
                "Image extensions which are allowed: jpg, jpe, jpeg, png, gif, svg, bmp, webp"
                in json_resp["result"]["error_template"]
            )

    def test_delete_card(self, client, app, auth):
        tarav = self.example_user(app, "tarav")

        with client:
            auth.login(tarav)
            card = self.get_posted_card(app)

            resp = client.post(
                "/delete-card",
                data={"card_id": card["card_id"], "deck_id": card["deck_id"]},
                follow_redirects=True,
            )
            assert resp.status_code == 200
