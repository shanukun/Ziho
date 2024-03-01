from flask import Blueprint

bp = Blueprint("ajax", __name__)

from ziho.ajax import views

bp.add_url_rule("/add-card", view_func=views.AddCard.as_view("add_card_route"))
bp.add_url_rule("/get-cards", view_func=views.GetCards.as_view("get_cards"))
bp.add_url_rule(
    "/update-card-info",
    view_func=views.UpdateCardInfo.as_view("update_card_info_route"),
)
bp.add_url_rule("/update-card", view_func=views.UpdateCard.as_view("update_card_route"))
