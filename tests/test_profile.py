import pytest

from tests.lib.base import ZihoTest


class TestProfileView(ZihoTest):

    def test_profile_user(self, client, app, auth):
        dalinar = self.example_user(app, "dalinar")

        with client:
            auth.login(dalinar)
            decks = self.get_posted_decks(app)

            resp = client.get(f"/profile/{'dalinar'}")
            assert resp.status_code == 200

            html = resp.get_data(as_text=True)

            for deck in decks:
                assert deck["deck_name"] in html
                for tag in deck["tags"]:
                    assert tag in html

    def test_edit_profile_template(self, client, app, auth):
        szeth = self.example_user(app, "szeth")

        with client:
            auth.login(szeth)

            resp = client.get("/profile/edit-profile")
            assert resp.status_code == 200

            html = resp.get_data(as_text=True)
            assert 'action="/profile/edit-profile"' in html

    @pytest.mark.parametrize(
        ("username", "about_me", "message"),
        (
            ("szeth", "abc", b"Please use a different username"),
            ("new_username", "abc", b"Your changes have been saved"),
        ),
    )
    def test_edit_profile_input(self, client, auth, app, username, about_me, message):
        self.example_user(app, "szeth")
        dalinar = self.example_user(app, "dalinar")
        with client:
            auth.login(dalinar)

            resp = client.post(
                "/profile/edit-profile",
                data={
                    "username": username,
                    "about_me": about_me,
                },
            )
            assert message in resp.data

    def test_change_password_template(self, client, app, auth):
        szeth = self.example_user(app, "szeth")

        with client:
            auth.login(szeth)

            resp = client.get("/profile/change-password")
            assert resp.status_code == 200

            html = resp.get_data(as_text=True)
            assert 'action="/profile/change-password"' in html

    @pytest.mark.parametrize(
        ("old_pass", "new_pass", "new_pass2", "message"),
        (
            ("abcdefgh", "mnopqrst", "mnopqrst", b"Incorrent old password."),
            ("secret@123", "mnopqrst", "xyz", b"Field must be equal to password"),
            ("secret@123", "mnopqrst", "mnopqrst", b"Your password has been changed"),
        ),
    )
    def test_change_password_input(
        self, client, app, auth, old_pass, new_pass, new_pass2, message
    ):
        szeth = self.example_user(app, "szeth")
        with client:
            auth.login(szeth)
            resp = client.post(
                "/profile/change-password",
                data={
                    "old_password": old_pass,
                    "password": new_pass,
                    "password2": new_pass2,
                },
            )
            assert resp.status_code == 200
            print(resp.get_data(as_text=True))
            assert message in resp.data
