from datetime import datetime

from sqlalchemy import func

from ziho import db
from ziho.core.models import Card, CardInfo, Deck
from ziho.utils.db import try_commit


def create_deck_handler(user, form_data):
    deck = Deck(name=form_data["deck_name"], creator_id=user.id)
    db.session.add(deck)
    try_commit(db.session, f'Could not create deck {form_data["deck_name"]}')


def delete_deck_handler(user, form_data):
    print(form_data)
    deck = db.session.execute(
        db.select(Deck).where(
            (Deck.id == form_data["deck_id"]) & (Deck.creator_id == user.id)
        )
    ).scalar_one_or_none()
    if deck:
        db.session.delete(deck)
        try_commit(db.session, f"Could not delete the deck. {deck.name}.")


def get_cards_for_deck(deck_id: int, type: str | None = None):
    stmt = db.select(Card).where(Card.deck_id == deck_id)
    cards = db.session.execute(stmt).all()
    if type == "dict":
        return {card.id: card for (card,) in cards}
    return [card for (card,) in cards]


def get_decks_by_user(user_id: int, type: str | None = None):
    base_subq = db.select(Card.deck_id, func.count().label("count")).join(
        CardInfo, CardInfo.card_id == Card.id
    )
    subq = (
        lambda states: base_subq.where(CardInfo.state.in_(states))
        .group_by(Card.deck_id, CardInfo.state)
        .subquery()
    )

    new_subq = subq([0])
    learning_subq = subq([1, 3])
    due_subq = (
        base_subq.group_by(Card.deck_id)
        .where(CardInfo.due <= datetime.now())
        .subquery()
    )

    stmt = (
        db.select(
            Deck.id,
            Deck.name,
            db.case((new_subq.c.count == None, 0), else_=new_subq.c.count).label("new"),
            db.case(
                (learning_subq.c.count == None, 0), else_=learning_subq.c.count
            ).label("learning"),
            db.case((due_subq.c.count == None, 0), else_=due_subq.c.count).label("due"),
        )
        .outerjoin(new_subq, Deck.id == new_subq.c.deck_id)
        .outerjoin(learning_subq, Deck.id == learning_subq.c.deck_id)
        .outerjoin(due_subq, Deck.id == due_subq.c.deck_id)
        .where(Deck.creator_id == user_id)
    )

    deck_rows = db.session.execute(stmt).all()

    if type == "dict":
        return {deck.id: deck for deck in deck_rows}
    return [deck for deck in deck_rows]


def get_card_info_by_id(card_info_id: int, card_id: int, deck_id: int):
    return db.session.execute(
        db.select(CardInfo.id)
        .join(CardInfo.parent_card)
        .join(Card.parent_deck)
        .where(Card.id == card_id)
        .where(Card.deck_id == deck_id)
        .where(CardInfo.id == card_info_id)
    ).scalar_one_or_none()


def get_deck_by_id(deck_id: int):
    return db.session.execute(
        db.select(Deck).where(Deck.id == deck_id)
    ).scalar_one_or_none()


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
