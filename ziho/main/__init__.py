from flask import Blueprint

from ziho.main.views import EditProfile, Home, User, ViewChoosenDeck, ViewDeck

bp = Blueprint("main", __name__)


bp.add_url_rule("/", view_func=Home.as_view(""))
bp.add_url_rule("/home", view_func=Home.as_view("home"))

bp.add_url_rule("/user/<username>", view_func=User.as_view("user"))

bp.add_url_rule("/view-deck", view_func=ViewDeck.as_view("view_deck"))
bp.add_url_rule(
    "/view-deck/<int:deck_id>", view_func=ViewChoosenDeck.as_view("view_choosen_deck")
)

bp.add_url_rule("/edit-profile", view_func=EditProfile.as_view("edit_profile"))
