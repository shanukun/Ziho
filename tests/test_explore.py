from urllib.parse import urlparse

from flask_login import current_user

from tests.lib.base import ZihoTest
from ziho.profile.handlers import get_decks_by_user


class TestExploreView(ZihoTest):
    def test_explore_without_login(self, client):
        resp = client.get("/explore")
        assert resp.status_code == 302
        assert urlparse(resp.headers["Location"]).path == "/auth/login"

    def test_explore_empty_template(self, client, app, auth):
        adolin = self.example_user(app, "adolin")
        auth.login(adolin)

        resp = client.get("/explore")
        assert resp.status_code == 200

        html = resp.get_data(as_text=True)
        assert "No decks to show" in html

    def test_explore(self, client, app, auth):
        jasnah = self.example_user(app, "jasnah")
        with client:
            auth.login(jasnah)
            decks = self.get_posted_decks(app)

        szeth = self.example_user(app, "szeth")
        with client:
            auth.login(szeth)
            resp = client.get("/explore")
            assert resp.status_code == 200

            html = resp.get_data(as_text=True)
            assert 'action="/clone-deck"' in html

            for deck in decks:
                assert deck["deck_name"] in html

    def test_clone_deck(self, client, app, auth):
        jasnah = self.example_user(app, "jasnah")
        with client:
            auth.login(jasnah)
            decks = self.get_posted_decks(app)

        szeth = self.example_user(app, "szeth")
        with client:
            auth.login(szeth)
            resp = client.post(
                "/clone-deck", data={"deck_id": decks[0]["id"]}, follow_redirects=True
            )
            assert resp.status_code == 200
            with app.app_context():
                user_decks = get_decks_by_user(current_user.id)
                assert decks[0]["deck_name"] == user_decks[0].name
