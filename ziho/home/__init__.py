from flask import Blueprint

from ziho.home import views

bp = Blueprint("home", __name__)


bp.add_url_rule("/", view_func=views.Home.as_view(""))
bp.add_url_rule("/home", view_func=views.Home.as_view("home"))

bp.add_url_rule("/add-card", view_func=views.AddCard.as_view("add_card_route"))
bp.add_url_rule("/create-deck", view_func=views.CreateDeck.as_view("create_deck_route"))
bp.add_url_rule("/delete-deck", view_func=views.DeleteDeck.as_view("delete_deck_route"))
bp.add_url_rule("/get-cards", view_func=views.GetCards.as_view("get_cards"))
bp.add_url_rule("/update-card-info", view_func=views.UpdateCardInfo.as_view("update_card_info_route"),)

bp.add_url_rule("/user/<username>", view_func=views.User.as_view("user"))
bp.add_url_rule("/edit-profile", view_func=views.EditProfile.as_view("edit_profile"))

bp.add_url_rule("/ziho_uploads/<image_name>", view_func=views.ShowImage.as_view("show_image"))
