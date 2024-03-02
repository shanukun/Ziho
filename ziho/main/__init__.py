from flask import Blueprint

from ziho.main import views

bp = Blueprint("main", __name__)


bp.add_url_rule("/", view_func=views.Home.as_view(""))
bp.add_url_rule("/home", view_func=views.Home.as_view("home"))
bp.add_url_rule("/user/<username>", view_func=views.User.as_view("user"))
bp.add_url_rule("/view-deck", view_func=views.ViewDeck.as_view("view_deck"))
bp.add_url_rule(
    "/view-deck/<int:deck_id>",
    view_func=views.ViewChoosenDeck.as_view("view_choosen_deck"),
)
bp.add_url_rule("/create-deck", view_func=views.CreateDeck.as_view("create_deck_route"))
bp.add_url_rule("/delete-deck", view_func=views.DeleteDeck.as_view("delete_deck_route"))
bp.add_url_rule("/delete-card", view_func=views.DeleteCard.as_view("delete_card_route"))
bp.add_url_rule("/edit-profile", view_func=views.EditProfile.as_view("edit_profile"))
