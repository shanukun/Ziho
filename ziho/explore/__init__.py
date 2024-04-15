from flask import Blueprint

from ziho.explore import views

bp = Blueprint("explore", __name__)


bp.add_url_rule("/explore", view_func=views.Explore.as_view("explore"))
bp.add_url_rule(
    "/view_deck/<int:deck_id>", view_func=views.ViewDeck.as_view("view_deck")
)
bp.add_url_rule("/clone-deck", view_func=views.CloneDeck.as_view("clone_deck"))
