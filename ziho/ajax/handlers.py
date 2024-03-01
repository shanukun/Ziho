import os
from datetime import datetime

from flask import url_for
from sqlalchemy.orm import Bundle
from werkzeug.utils import secure_filename

from ziho import db
from ziho.core.models import Card, CardInfo, Deck
from ziho.utils.db import try_commit


# TODO temp sol, use more robust approach for saving images
# Put in image utils
def save_image(app, image_data):
    filename = secure_filename(image_data.filename)
    full_path = os.path.join(app.config["UPLOAD_PATH"], filename)
    image_data.save(full_path)
    return url_for("ajax.show_image", image_name=filename, _external=True)


def get_image_path(app, image):
    image_path = None
    if image:
        image_path = save_image(app, image)
    return image_path


def create_card_handler(app, user, form_data):
    card = Card(
        front=form_data["front"],
        back=form_data["back"],
        deck_id=form_data["deck_id"],
        image_path=get_image_path(app, form_data["card_image"]),
    )
    card_info = CardInfo(parent_card=card, user_id=user.id)
    db.session.add(card)
    db.session.add(card_info)

    try_commit(db.session, f'Could not create the card: {form_data["front"]}.')


def get_cards_for_study(form_data, user_id: int):
    stmt = (
        db.select(
            Bundle("deck", Deck.id.label("deck_id")),
            Bundle(
                "card", Card.id.label("card_id"), Card.front, Card.back, Card.image_path
            ),
            Bundle(
                "card_info",
                CardInfo.id.label("card_info_id"),
                CardInfo.difficulty,
                CardInfo.due,
                CardInfo.elapsed_days,
                CardInfo.lapses,
                CardInfo.last_review,
                CardInfo.reps,
                CardInfo.scheduled_days,
                CardInfo.stability,
                CardInfo.state,
            ),
        )
        .join(Card.parent_deck)
        .join(Card.card_info)
        .where((Deck.id == form_data["deck_id"]) & (Deck.creator_id == user_id))
        .where(CardInfo.due <= datetime.now())
        .order_by(CardInfo.due)
        .limit(20)
    )

    due_cards = []
    for study_card in db.session.execute(stmt):
        study_card_dict = study_card._mapping

        due_card = {}
        for bundle in study_card_dict:
            due_card[bundle] = {
                k: v for k, v in study_card_dict[bundle]._mapping.items()
            }

        due_cards.append(due_card)

    return due_cards


def update_card_handler(app, user, form_data):
    base_stmt = (
        db.update(Card)
        .where(Card.deck_id == form_data["deck_id"])
        .where(Card.id == form_data["card_id"])
        .where(
            user.id
            == db.select(Deck.creator_id)
            .where(Deck.id == form_data["deck_id"])
            .scalar_subquery()
        )
    )

    data_stmt = base_stmt.values(
        front=form_data["front"],
        back=form_data["back"],
    )

    image_path = get_image_path(app, form_data["card_image"])
    if image_path:
        image_stmt = base_stmt.values(image_path=image_path)
        db.session.execute(image_stmt)

    db.session.execute(data_stmt)
    try_commit(db.session, f"Could not update the card.")


def update_card_info_handler(user, form_data):
    stmt = (
        db.update(CardInfo)
        .where(CardInfo.id == form_data["card_info_id"])
        .where(CardInfo.card_id == form_data["card_id"])
        .where(
            user.id
            == db.select(Deck.creator_id)
            .where(Deck.id == form_data["deck_id"])
            .scalar_subquery()
        )
        .values(
            difficulty=form_data["difficulty"],
            due=form_data["due"],
            elapsed_days=form_data["elapsed_days"],
            lapses=form_data["lapses"],
            last_review=form_data["last_review"],
            reps=form_data["reps"],
            scheduled_days=form_data["scheduled_days"],
            stability=form_data["stability"],
            state=form_data["state"],
        )
    )
    db.session.execute(stmt)
    try_commit(db.session, f"Could not update the card info.")
