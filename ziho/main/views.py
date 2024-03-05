from flask import abort, flash, redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user, login_required

from ziho import db
from ziho.auth.handlers import get_user_or_404
from ziho.core.exceptions import PersistenceError
from ziho.core.forms import (
    AddCardForm,
    CardDeleteForm,
    CardForm,
    DeckDeleteForm,
    DeckForm,
    EditProfileForm,
)
from ziho.main.handlers import (
    create_deck_handler,
    delete_card_handler,
    delete_deck_handler,
    get_cards_for_deck,
    get_deck_by_id,
    get_decks_by_user,
)


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
        return redirect(url_for("main.home"))


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
        return redirect(url_for("main.home"))


class User(MethodView):
    decorators = [login_required]

    def get(self, username):
        user = get_user_or_404(username)
        decks = get_decks_by_user(user.id)
        return render_template("user.html", user=user, decks=decks)


class ViewDeckTemplate(MethodView):
    decorators = [login_required]

    def __init__(self):
        self.card_form = CardForm()
        self.card_delete_form = CardDeleteForm()

    def render(self, deck_id, decks=None):
        if not decks:
            decks = get_decks_by_user(current_user.id, "dict")

        cards = get_cards_for_deck(deck_id)
        return render_template(
            "view_deck.html",
            deck_id=deck_id,
            decks=decks,
            cards=cards,
            card_form=self.card_form,
            cd_form=self.card_delete_form,
        )


class ViewDeck(ViewDeckTemplate):
    def get(self):
        decks = get_decks_by_user(current_user.id, "dict")
        deck_id = None
        if decks:
            deck_id = next(iter(decks))

        return self.render(deck_id=deck_id, decks=decks)


class ViewChoosenDeck(ViewDeckTemplate):
    def get(self, deck_id):
        if not get_deck_by_id(deck_id):
            abort(404)

        return self.render(deck_id=deck_id)


class DeleteCard(MethodView):
    decorators = [login_required]

    def post(self):
        form = CardDeleteForm()
        if form.validate_on_submit():
            try:
                delete_card_handler(current_user, form.get_data())
                flash("Card deleted.", "success")
            except PersistenceError as e:
                flash(e.message, "danger")
        return redirect(request.referrer)


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
            return redirect(url_for("main.edit_profile"))

    def form(self):
        return EditProfileForm(current_user.username)
