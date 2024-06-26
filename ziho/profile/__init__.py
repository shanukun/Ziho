from flask import Blueprint

from ziho.profile import views

bp = Blueprint("profile", __name__)

bp.add_url_rule("/profile/<username>", view_func=views.User.as_view("user"))
bp.add_url_rule(
    "/profile/edit-profile", view_func=views.EditProfile.as_view("edit_profile")
)
bp.add_url_rule(
    "/profile/change-password",
    view_func=views.ChangePassword.as_view("change_password"),
)
