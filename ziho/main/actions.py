from datetime import datetime

from sqlalchemy.orm import Bundle

from ziho import db
from ziho.models import Card, CardInfo, Deck


def create_deck(deck_name: str | None, user_id: int):
    # TODO a decorator for removing whitespaces from all string
    deck_name = deck_name.strip()
    deck = Deck(name=deck_name, creator_id=user_id)
    db.session.add(deck)
    db.session.commit()
    return deck.id


def create_card(
    deck_id: int, front: str, back: str, user_id: int, image_path: str | None = None
):
    card = Card(front=front, back=back, deck_id=deck_id, image_path=image_path)
    card_info = CardInfo(parent_card=card, user_id=user_id)
    db.session.add(card)
    db.session.add(card_info)
    db.session.commit()
    return card.id


def get_cards_for_deck(deck_id: int, type: str | None = None):
    stmt = db.select(Card).where(Card.deck_id == deck_id)
    cards = db.session.execute(stmt).all()
    if type == "dict":
        return {card.id: card for (card,) in cards}
    return [card for (card,) in cards]


def get_cards_for_study(deck_id: int, user_id: int):
    stmt = (
        db.select(
            Bundle("deck", Deck.id),
            Bundle("card", Card.id, Card.front, Card.back, Card.image_path),
            Bundle(
                "card_info",
                CardInfo.id,
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
        .where((Deck.id == deck_id) & (CardInfo.user_id == user_id))
        .where(CardInfo.due <= datetime.now())
        .order_by(CardInfo.due)
        .limit(20)
    )

    due_cards = []
    for card in db.session.execute(stmt):
        # use _mapping and loop to fill dict
        due_cards.append(
            {
                "deck_id": card.deck.id,
                "card_id": card.card.id_1,
                "front": card.card.front,
                "back": card.card.back,
                "image_path": card.card.image_path,
                "card_info": {
                    "card_info_id": card.card_info.id_2,
                    "difficulty": card.card_info.difficulty,
                    "due": card.card_info.due,
                    "elapsed_days": card.card_info.elapsed_days,
                    "lapses": card.card_info.lapses,
                    "last_review": card.card_info.last_review,
                    "reps": card.card_info.reps,
                    "scheduled_days": card.card_info.scheduled_days,
                    "stability": card.card_info.stability,
                    "state": card.card_info.state,
                },
            }
        )

    return due_cards


def get_decks_by_user(user_id: int, type: str | None = None):
    decks_row = db.session.execute(
        db.select(Deck).where(Deck.creator_id == user_id)
    ).all()
    if type == "dict":
        return {deck.id: deck for (deck,) in decks_row}
    return [deck for (deck,) in decks_row]


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


def update_card(
    deck_id: int,
    card_id: int,
    front: str,
    back: str,
    user_id: int,
    image_path: str | None = None,
):
    base_stmt = (
        db.update(Card)
        .where(Card.deck_id == deck_id)
        .where(Card.id == card_id)
        .where(
            user_id
            == db.select(Deck.creator_id).where(Deck.id == deck_id).scalar_subquery()
        )
    )

    data_stmt = base_stmt.values(
        front=front,
        back=back,
    )

    if image_path:
        image_stmt = base_stmt.values(image_path=image_path)
        db.session.execute(image_stmt)

    db.session.execute(data_stmt)
    db.session.commit()


def delete_card(deck_id: int, card_id: int, user_id: int):
    card = db.session.execute(
        db.select(Card)
        .where(Card.deck_id == deck_id)
        .where(Card.id == card_id)
        .where(
            user_id
            == db.select(Deck.creator_id).where(Deck.id == deck_id).scalar_subquery()
        )
    ).scalar_one_or_none()
    db.session.delete(card)
    db.session.commit()


def update_card_info(card_info_dict: dict):
    stmt = (
        db.update(CardInfo)
        .where(CardInfo.id == card_info_dict["card_info_id"])
        .where(CardInfo.card_id == card_info_dict["card_id"])
        .values(
            difficulty=card_info_dict["difficulty"],
            due=card_info_dict["due"],
            elapsed_days=card_info_dict["elapsed_days"],
            lapses=card_info_dict["lapses"],
            last_review=card_info_dict["last_review"],
            reps=card_info_dict["reps"],
            scheduled_days=card_info_dict["scheduled_days"],
            stability=card_info_dict["stability"],
            state=card_info_dict["state"],
        )
    )
    db.session.execute(stmt)
    db.session.commit()
