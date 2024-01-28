import os

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ziho import db
from ziho.auth.actions import get_user_or_404
from ziho.main import bp
from ziho.main.actions import (
    create_card,
    create_deck,
    get_cards_for_deck,
    get_decks_by_user,
    update_card_info,
)
from ziho.main.forms import (
    CardCreationForm,
    CardForm,
    CardInfoForm,
    CardResponseForm,
    DeckForm,
    EditProfileForm,
    GetCardReqForm,
)


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


@bp.route("/create_deck", methods=["POST"])
@login_required
def create_deck_route():
    form = DeckForm()
    if form.validate_on_submit():
        create_deck(form.deck_name.data, current_user.id)
        return redirect(url_for("main.home"))
    return "<h1>Failed</h1>"


# TODO temp sol, use more robust approach for saving images
def save_image(image_data):
    filename = secure_filename(image_data.filename)
    full_path = os.path.join(current_app.config["UPLOAD_PATH"], filename)
    image_data.save(full_path)
    return url_for("main.show_image", image_name=filename, _external=True)


@bp.route("/ziho_uploads/<image_name>")
@login_required
def show_image(image_name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], image_name)


@bp.route("/add-card", methods=["POST"])
@login_required
def add_card_route():
    form = CardCreationForm()
    if form.validate_on_submit():
        image_path = None
        if form.image and form.image.data:
            image_path = save_image(form.image.data)
        create_card(
            form.deck.data, form.front.data, form.back.data, current_user.id, image_path
        )
        return "<h1>Passed</h1>"
    return "<h1>Failed</h1>"
    # TODO generate better response with error and confirmation message


@bp.route("/get-cards", methods=["POST"])
@login_required
def get_cards():
    form = GetCardReqForm()
    if form.validate_on_submit():
        return {
            "status": True,
            "result": get_cards_for_deck(form.deck_id.data, current_user.id),
        }
    print(form.errors)
    return {"status": False, "msg": "Invalid deck id."}


# TODO change to update card info
@bp.route("/save-card", methods=["POST"])
@login_required
def save_card():
    form = CardInfoForm()
    if form.validate_on_submit():
        # add func to forms
        card_info_dict = dict()
        for k in dict(form._fields):
            card_info_dict[k] = form._fields[k].data
        update_card_info(card_info_dict)
        return {"msg": "Valid deck id and card id."}

    # TODO not a valid method
    error_string = ""
    for k in form.errors:
        if k is not None:
            for emsg in form.errors[k]:
                error_string += k + ": " + emsg + "\n"
    # TODO use abort for api errors
    return {"msg": error_string}


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
