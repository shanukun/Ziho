from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask.views import MethodView
from flask_login import current_user, login_required

from ziho import db
from ziho.auth.handlers import get_user_or_404
from ziho.core.exceptions import PersistenceError
from ziho.core.forms import (
    CardForm,
    CardInfoForm,
    DeckDeleteForm,
    DeckForm,
    EditProfileForm,
    GetCardsRequestForm,
)
from ziho.core.utils import FormPost
from ziho.errors.errors import InvalidFormData, ServerError
from ziho.home.handlers import (
    create_card_handler,
    create_deck_handler,
    delete_deck_handler,
    get_cards_for_study,
    get_decks_by_user,
    update_card_info_handler,
    update_profile,
)
from ziho.utils.helper import get_handler_caller, get_response


class Home(MethodView):
    decorators = [login_required]

    def get(self):
        decks = get_decks_by_user(current_user.id)

        deck_form, card_form = DeckForm(), CardForm()
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
    form_template = "_forms/create_deck.html"
    form_name = "deck_form"
    success_message = "New deck created."

    def post(self):
        form = DeckForm()
        handler_caller = get_handler_caller(
            create_deck_handler, current_user, form.get_data()
        )
        form_post = FormPost(
            handler_caller,
            form,
            self.form_template,
            self.form_name,
            self.success_message,
        )
        return form_post.do_post()


class AddCard(MethodView):
    decorators = [login_required]
    form_template = "_forms/add_card.html"
    form_name = "card_form"
    success_message = "Card added."

    def post(self):
        form = self.form()
        handler_caller = get_handler_caller(
            create_card_handler, current_app, current_user, form.get_data()
        )
        form_post = FormPost(
            handler_caller,
            form,
            self.form_template,
            self.form_name,
            self.success_message,
        )
        return form_post.do_post()

    def form(self):
        form = CardForm()
        form.add_choices(get_decks_by_user(current_user.id))
        return form


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
            return get_response(
                result=get_cards_for_study(form.get_data(), current_user.id)
            )
        else:
            raise InvalidFormData("Invalid form data.")


class UpdateCardInfo(MethodView):
    decorators = [login_required]

    def post(self):
        form = CardInfoForm(meta={"csrf": False})
        if form.validate_on_submit():
            try:
                update_card_info_handler(current_user, form.get_data())
            except PersistenceError as e:
                raise ServerError(e.message)
            return get_response(message="Card info updated.")
        else:
            raise InvalidFormData("Invalid form data.")


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
            try:
                update_profile(current_user, form.get_data())
                flash("Your changes have been saved.", "success")
            except PersistenceError as e:
                flash(e.message, "danger")
            return redirect(url_for("home.edit_profile"))
        else:
            return render_template("edit_profile.html", title="Edit Profile", form=form)

    def form(self):
        return EditProfileForm(current_user.username)
