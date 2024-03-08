from ziho import db
from ziho.core.models import Card, Deck
from ziho.utils.db import try_commit
from ziho.utils.image import get_image_path


def get_cards_for_deck(deck_id: int, type: str | None = None):
    stmt = db.select(Card).where(Card.deck_id == deck_id)
    cards = db.session.execute(stmt).all()
    if type == "dict":
        return {card.id: card for (card,) in cards}
    return [card for (card,) in cards]


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
    try_commit(db.session, "Could not update the card.")


def delete_card_handler(user, form_data):
    card = db.session.execute(
        db.select(Card)
        .where(Card.deck_id == form_data["deck_id"])
        .where(Card.id == form_data["card_id"])
        .where(
            user.id
            == db.select(Deck.creator_id)
            .where(Deck.id == form_data["deck_id"])
            .scalar_subquery()
        )
    ).scalar_one_or_none()
    if card:
        db.session.delete(card)
        try_commit(db.session, f"Could not delete the card {card.front}.")
