from flask import current_app, jsonify, redirect, send_from_directory, url_for
from flask.views import MethodView
from flask_login import current_user, login_required

from ziho.ajax import bp
from ziho.ajax.handlers import (
    create_card_handler,
    create_deck_handler,
    delete_card_handler,
    get_cards_for_study,
    update_card_handler,
    update_card_info_handler,
)
from ziho.core.exceptions import PersistenceError
from ziho.core.forms import (
    CardCreationForm,
    CardDeleteForm,
    CardInfoForm,
    CardUpdateForm,
    DeckForm,
    GetCardsRequestForm,
)
from ziho.errors.errors import AjaxError, InvalidFormData, ServerError


def get_success_response(message=None, result=None):
    return {"message": message, "result": result}


@bp.errorhandler(AjaxError)
def invalid_api_usage(e):
    print(e.to_dict())
    return jsonify(e.to_dict()), e.status_code


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


class GetCards(MethodView):
    decorators = [login_required]

    def post(self):
        form = GetCardsRequestForm(meta={"csrf": False})
        if form.validate_on_submit():
            return get_success_response(
                result=get_cards_for_study(form.get_data(), current_user.id)
            )
        raise InvalidFormData(form.errors)


class DeleteCard(MethodView):
    decorators = [login_required]

    def post(self):
        form = CardDeleteForm()
        if form.validate_on_submit():
            try:
                delete_card_handler(current_user, form.get_data())
            except PersistenceError as e:
                raise ServerError(e.message)
            return get_success_response(result="Card Deleted.")
        raise InvalidFormData(form.errors)


class CreateDeck(MethodView):
    decorators = [login_required]

    def post(self):
        form = DeckForm()
        if form.validate_on_submit():
            try:
                create_deck_handler(current_user, form.get_data())
            except PersistenceError as e:
                raise ServerError(e.message)
            return redirect(url_for("main.home"))
        raise InvalidFormData(form.errors)


@bp.route("/ziho_uploads/<image_name>")
@login_required
def show_image(image_name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], image_name)


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
