from flask import flash, redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user, login_required

from ziho.core.exceptions import PersistenceError
from ziho.core.forms import DeckIdForm
from ziho.core.handler import get_deck_by_id
from ziho.deckview.handlers import get_cards_for_deck
from ziho.explore.handlers import clone_deck, get_decks


class Explore(MethodView):
    decorators = [login_required]

    def get(self):
        did_form = DeckIdForm()
        page = request.args.get("page", 1, type=int)
        decks = get_decks(page)

        return render_template("explore.html", decks=decks, did_form=did_form)


class ViewDeck(MethodView):
    decorators = [login_required]
    template = "view_deck_non_user.html"

    def get(self, deck_id):
        cards = get_cards_for_deck(deck_id)
        deck = get_deck_by_id(deck_id)
        if deck and current_user.id == deck.creator_id:
            return redirect(url_for("deckview.view_deck", deck_id=deck.id))

        return render_template(
            self.template, deck_id=deck_id, current_deck=deck, cards=cards
        )


class CloneDeck(MethodView):
    decorators = [login_required]

    def post(self):
        form = DeckIdForm()
        if form.validate_on_submit():
            try:
                clone_deck(current_user, form.get_data())
                flash("Deck Cloned.", "success")
            except PersistenceError as e:
                flash(e.message, "danger")
        return redirect(url_for("explore.explore"))
