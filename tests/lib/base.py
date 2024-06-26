import functools
import random
import string
from pathlib import Path

from flask_login import current_user
from werkzeug.datastructures import FileStorage

from ziho.auth.handlers import create_user, get_user_by_username
from ziho.home.handlers import create_card_handler, create_deck_handler

IMAGE_DIR = Path(__file__).parent.parent / "data" / "images"
TEST_IMAGE = "test_image.png"
TEST_IMAGE_XYZ = "test_image_xyz.xyz"


def push_app_context(func):
    @functools.wraps(func)
    def wrapper(cls, app, *args, **kwargs):
        with app.app_context():
            return func(cls, app, *args, **kwargs)

    return wrapper


def generate_string(min, max):
    # TODO figure out why some of the strings containing string.punctuations can't be found in reponse html
    res = "".join(
        random.choices(string.ascii_letters + string.digits, k=random.randint(min, max))
    )
    return res.strip()


class ZihoTest:
    tags = ["abc", "xyz"]
    tags_str = ",".join(tags)
    password = "secret@123"
    example_user_map = dict(
        kaladin="kaladin@ziho.com",
        shallan="shallan@ziho.com",
        dalinar="dalinar@ziho.com",
        szeth="szeth@ziho.com",
        adolin="adolin@ziho.com",
        jasnah="jasnah@ziho.com",
        navani="navani@ziho.com",
        moash="moash@ziho.com",
        tarav="tarav@ziho.com",
    )

    nonreg_user_map = dict(
        vasher="vasher@email.com",
        vivenna="vivenna@email.com",
        siri="siri@email.com",
        lightsong="lightsong@email.com",
        susebron="susebron@email.com",
        blushweaver="blushweaver@email.com",
        nightblood="nightblood@email.com",
    )

    def _user_to_json(self, user, all_info=False):
        user_json = dict(username=user, password=self.password)
        if user in self.nonreg_user_map:
            user_json |= {
                "email": self.nonreg_user_map[user],
                "password2": self.password,
            }
        if all_info:
            user_json |= {
                "email": self.example_user_map[user],
                "password2": self.password,
            }
        return user_json

    @push_app_context
    def example_user(self, app, username, all_info=False):
        if not get_user_by_username(username):
            create_user(username, self.example_user_map[username], self.password)
        return self._user_to_json(username, all_info)

    @push_app_context
    def get_user(self, app, username):
        self.example_user(app, username)
        return get_user_by_username(username)

    def nonreg_user(self, username):
        return self._user_to_json(username)

    def get_deck(self):
        return {
            "deck_name": generate_string(5, 30),
            "tags": self.tags_str,
            "tag_list": self.tags,
        }

    @push_app_context
    def get_posted_deck(self, app):
        deck = self.get_deck()

        deck["tags"] = deck["tag_list"]
        del deck["tag_list"]

        deck_id = create_deck_handler(current_user, deck)
        deck |= {"id": deck_id}
        return deck

    @push_app_context
    def get_posted_decks(self, app, count=2):
        decks = []
        for _ in range(count):
            deck = self.get_posted_deck(app)
            create_card_handler(
                app, current_user, self.get_card(deck["id"], False, True)
            )
            decks.append(deck)

        return decks

    def get_card(self, id, image=False, valid_ext=True):
        card_image = None
        image_file = TEST_IMAGE
        image_path = IMAGE_DIR / TEST_IMAGE
        if image:
            if not valid_ext:
                image_path = IMAGE_DIR / TEST_IMAGE_XYZ
                image_file = TEST_IMAGE_XYZ
            card_image = FileStorage(image_path.open("rb"), filename=image_file)
        return {
            "deck_id": id,
            "front": generate_string(15, 50),
            "back": generate_string(30, 100),
            "card_image": card_image,
        }

    @push_app_context
    def get_posted_card(self, app, image=False, valid_ext=True):
        deck = self.get_posted_deck(app)
        card = self.get_card(deck["id"], image, valid_ext)
        card_id = create_card_handler(app, current_user, card)
        card |= {"deck_id": deck["id"], "card_id": card_id}
        return card
