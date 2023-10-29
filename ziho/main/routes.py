from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ziho import db
from ziho.auth.actions import get_user_or_404
from ziho.main import bp
from ziho.main.actions import create_card, create_deck, get_decks_by_user
from ziho.main.forms import CardForm, CardResponseForm, DeckForm, EditProfileForm


@bp.route("/")
@bp.route("/home")
@login_required
def home():
    decks = get_decks_by_user(current_user.id)

    deck_form = DeckForm()
    card_form = CardForm()
    card_form.deck.choices = [(deck.id, deck.name) for deck in decks]

    return render_template(
        "home.html", title="Home", decks=decks, deck_form=deck_form, card_form=card_form
    )


@bp.route("/user/<username>")
@login_required
def user(username):
    user = get_user_or_404(username)
    decks = get_decks_by_user(user.id)
    return render_template("user.html", user=user, decks=decks)


@bp.route("/deck", methods=["POST"])
@login_required
def deck():
    form = DeckForm()
    if form.validate_on_submit():
        create_deck(form.deck_name.data, current_user.id)
        return redirect(url_for("main.home"))


@bp.route("/card", methods=["POST"])
@login_required
def card():
    form = CardResponseForm()
    if form.validate_on_submit():
        create_card(form.deck.data, form.front.data, form.back.data)
        return "<h1>Passed</h1>"
    return "<h1>Failed</h1>"


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)
