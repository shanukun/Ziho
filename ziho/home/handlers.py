from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Bundle

from ziho import db
from ziho.core.models import Card, CardInfo, Deck, User
from ziho.utils.db import try_commit
from ziho.utils.image import get_image_path


def update_profile(user, form_data):
    stmt = (
        db.update(User)
        .where(User.id == user.id)
        .values(username=form_data["username"], about_me=form_data["about_me"])
    )

    db.session.execute(stmt)

    try_commit(db.session, "Could not update profile.")


def create_deck_handler(user, form_data):
    deck = Deck(name=form_data["deck_name"], creator_id=user.id)
    db.session.add(deck)
    try_commit(db.session, f'Could not create deck {form_data["deck_name"]}')
    return deck.id


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
    return card.id


def delete_deck_handler(user, form_data):
    deck = db.session.execute(
        db.select(Deck).where(
            (Deck.id == form_data["deck_id"]) & (Deck.creator_id == user.id)
        )
    ).scalar_one_or_none()
    if deck:
        db.session.delete(deck)
        try_commit(db.session, f"Could not delete the deck. {deck.name}.")


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
    for study_card in db.session.execute(stmt).all():
        study_card_dict = study_card._mapping

        due_card = {}
        for bundle in study_card_dict:
            due_card[bundle] = {
                k: v for k, v in study_card_dict[bundle]._mapping.items()
            }

        due_cards.append(due_card)

    return due_cards


def get_decks_by_user(user_id: int, type: str | None = None):
    decks = db.session.execute(
        db.select(Deck).where(Deck.creator_id == user_id)
    ).scalars()
    if type == "dict":
        return {deck.id: deck for deck in decks}
    return [deck for deck in decks]


# TODO use different function for deck id and name
def get_decks_by_user_with_stats(user_id: int):
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

    return [deck for deck in deck_rows]


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
    try_commit(db.session, "Could not update the card info.")
