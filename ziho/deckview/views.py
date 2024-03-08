from flask import abort, current_app, flash, redirect, render_template, request
from flask.views import MethodView
from flask_login import current_user, login_required

from ziho.core.exceptions import PersistenceError
from ziho.core.forms import CardDeleteForm, CardForm, CardUpdateForm
from ziho.errors.errors import InvalidFormData, ServerError
from ziho.utils.helper import get_success_response
from ziho.deckview.handlers import (
    delete_card_handler,
    get_cards_for_deck,
    update_card_handler,
)
from ziho.home.handlers import get_decks_by_user
from ziho.core.handler import get_deck_by_id


# @bp.errorhandler(AjaxError)
# def invalid_api_usage(e):
#     print(e.to_dict())
#     return jsonify(e.to_dict()), e.status_code

class UpdateCard(MethodView):
    decorators = [login_required]

    def post(self):
        form = CardUpdateForm(meta={"csrf": False})
        if form.validate_on_submit():
            try:
                update_card_handler(current_app, current_user, form.get_data())
            except PersistenceError as e:
                raise ServerError(e.message)
            return get_success_response(message="Card updated.")
        raise InvalidFormData(form.errors)


class ViewDeckBase(MethodView):
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


class ViewDeck(ViewDeckBase):
    def get(self):
        decks = get_decks_by_user(current_user.id, "dict")
        deck_id = None
        if decks:
            deck_id = next(iter(decks))

        return self.render(deck_id=deck_id, decks=decks)


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
        return redirect(request.referrer)
