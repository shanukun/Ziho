from flask import abort, current_app, flash, redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user, login_required

from ziho.core.exceptions import PersistenceError
from ziho.core.forms import CardDeleteForm, CardUpdateForm
from ziho.core.handler import get_deck_by_id
from ziho.core.utils import FormPost
from ziho.deckview.handlers import (
    delete_card_handler,
    get_cards_for_deck,
    update_card_handler,
)
from ziho.profile.handlers import get_decks_by_user
from ziho.utils.helper import get_handler_caller


class UpdateCard(MethodView):
    decorators = [login_required]
    form_template = "_forms/update_card.html"
    form_name = "card_form"
    success_message = "Card updated."

    def post(self):
        form = CardUpdateForm()
        handler_caller = get_handler_caller(
            update_card_handler, current_app, current_user, form.get_data()
        )
        form_post = FormPost(
            handler_caller,
            form,
            self.form_template,
            self.form_name,
            self.success_message,
        )
        return form_post.do_post()


class ViewDeckBase(MethodView):
    decorators = [login_required]
    template = "view_deck.html"

    def __init__(self):
        self.card_form = CardUpdateForm()
        self.card_delete_form = CardDeleteForm()

    def render(self, deck_id=None):
        decks = get_decks_by_user(current_user.id, "dict")
        if not decks:
            return render_template(self.template)
        deck_id = deck_id if deck_id else next(iter(decks))
        self.card_form.set_deck_name(decks[deck_id].name)

        cards = get_cards_for_deck(deck_id)
        return render_template(
            self.template,
            deck_id=deck_id,
            current_deck=decks[deck_id],
            decks=decks,
            cards=cards,
            card_form=self.card_form,
            cd_form=self.card_delete_form,
        )


class ViewDeck(ViewDeckBase):
    def get(self):
        return self.render()


class ViewChoosenDeck(ViewDeckBase):
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
        if request.referrer:
            return redirect(request.referrer)
        else:
            return redirect(url_for("home.home"))
