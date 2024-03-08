from flask import Blueprint

bp = Blueprint("deckview", __name__)

from ziho.deckview import views

bp.add_url_rule("/view-deck", view_func=views.ViewDeck.as_view("view_deck"))
bp.add_url_rule(
    "/view-deck/<int:deck_id>",
    view_func=views.ViewChoosenDeck.as_view("view_choosen_deck"),
)

bp.add_url_rule("/delete-card", view_func=views.DeleteCard.as_view("delete_card_route"))
bp.add_url_rule("/update-card", view_func=views.UpdateCard.as_view("update_card_route"))
