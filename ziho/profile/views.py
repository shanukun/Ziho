from flask import flash, render_template
from flask.views import MethodView
from flask_login import current_user, login_required

from ziho.auth.handlers import get_user_or_404
from ziho.core.exceptions import PersistenceError
from ziho.profile.forms import ChangePasswordForm, EditProfileForm
from ziho.profile.handlers import change_password, get_decks_by_user, update_profile


class User(MethodView):
    decorators = [login_required]

    def get(self, username):
        user = get_user_or_404(username)
        decks = get_decks_by_user(user.id)
        return render_template("profile.html", user=user, decks=decks)


class EditProfile(MethodView):
    decorators = [login_required]

    def get(self):
        form = self.form()
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        return self.render(form)

    def post(self):
        form = self.form()
        if form.validate_on_submit():
            try:
                update_profile(current_user, form.get_data())
                flash("Your changes have been saved.", "success")
            except PersistenceError as e:
                flash(e.message, "danger")
            return self.render(form)
        else:
            return self.render(form)

    def render(self, form):
        return render_template("edit_profile.html", title="Edit Profile", form=form)

    def form(self):
        return EditProfileForm(current_user.username)


class ChangePassword(MethodView):
    decorators = [login_required]

    def get(self):
        return self.render(self.form())

    def post(self):
        form = self.form()
        if form.validate_on_submit():
            try:
                change_password(current_user, form.get_data())
                flash("Your password has been changed.", "success")
            except PersistenceError as e:
                flash(e.message, "dange")
            return self.render(form)
        else:
            return self.render(form)

    def render(self, form):
        return render_template(
            "change_password.html", title="Change Password", form=form
        )

    def form(self):
        return ChangePasswordForm()
