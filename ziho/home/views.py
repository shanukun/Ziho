from flask import flash, redirect, render_template, send_from_directory, url_for, current_app
from flask.views import MethodView
from flask_login import current_user, login_required

from ziho import db
from ziho.auth.handlers import get_user_or_404
from ziho.core.exceptions import PersistenceError
from ziho.errors.errors import InvalidFormData, ServerError
from ziho.core.forms import (
    AddCardForm,
    CardCreationForm,
    CardInfoForm,
    GetCardsRequestForm,
    DeckDeleteForm,
    DeckForm,
    EditProfileForm,
)
from ziho.home.handlers import (
    create_card_handler,
    get_cards_for_study,
    update_card_info_handler,
    create_deck_handler,
    delete_deck_handler,
    get_decks_by_user,
)
from ziho.utils.helper import get_success_response


class Home(MethodView):
    decorators = [login_required]

    def get(self):
        decks = get_decks_by_user(current_user.id)

        deck_form, card_form = DeckForm(), AddCardForm()
        card_form.add_choices(decks)

        return render_template(
            "home.html",
            title="Home",
            decks=decks,
            deck_form=deck_form,
            card_form=card_form,
            dd_form=DeckDeleteForm(),
        )


class CreateDeck(MethodView):
    decorators = [login_required]

    def post(self):
        form = DeckForm()
        if form.validate_on_submit():
            try:
                create_deck_handler(current_user, form.get_data())
                flash("New deck created.", "success")
            except PersistenceError as e:
                flash(e.message, "danger")
        return redirect(url_for("home.home"))


class DeleteDeck(MethodView):
    decorators = [login_required]

    def post(self):
        form = DeckDeleteForm()
        if form.validate_on_submit():
            try:
                delete_deck_handler(current_user, form.get_data())
                flash("Deck Deleted", "success")
            except PersistenceError as e:
                flash(e.message, "danger")
        return redirect(url_for("home.home"))


class AddCard(MethodView):
    decorators = [login_required]

    def post(self):
        form = CardCreationForm()
        if form.validate_on_submit():
            try:
                create_card_handler(current_app, current_user, form.get_data())
            except PersistenceError as e:
                raise ServerError(e.message)
            return get_success_response(message="Card added.")
        raise InvalidFormData(form.errors)


class ShowImage(MethodView):
    decorators = [login_required]

    def get(self, image_name):
        return send_from_directory(current_app.config["UPLOAD_FOLDER"], image_name)


class User(MethodView):
    decorators = [login_required]

    def get(self, username):
        user = get_user_or_404(username)
        decks = get_decks_by_user(user.id)
        return render_template("profile.html", user=user, decks=decks)


class GetCards(MethodView):
    decorators = [login_required]

    def post(self):
        form = GetCardsRequestForm(meta={"csrf": False})
        if form.validate_on_submit():
            return get_success_response(
                result=get_cards_for_study(form.get_data(), current_user.id)
            )
        raise InvalidFormData(form.errors)


class UpdateCardInfo(MethodView):
    decorators = [login_required]

    def post(self):
        form = CardInfoForm(meta={"csrf": False})
        if form.validate_on_submit():
            try:
                update_card_info_handler(current_user, form.get_data())
            except PersistenceError as e:
                raise ServerError(e.message)
            return get_success_response(message="Card info updated.")
        raise InvalidFormData(form.errors)


class EditProfile(MethodView):
    decorators = [login_required]

    def get(self):
        form = self.form()
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        return render_template("edit_profile.html", title="Edit Profile", form=form)

    def post(self):
        form = self.form()
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash("Your changes have been saved.")
            return redirect(url_for("home.edit_profile"))

    def form(self):
        return EditProfileForm(current_user.username)
