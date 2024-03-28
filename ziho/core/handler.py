from ziho import db
from ziho.core.models import Card, CardInfo, Deck


def get_deck_by_id(deck_id: int):
    return db.session.execute(
        db.select(Deck).where(Deck.id == deck_id)
    ).scalar_one_or_none()


def get_card_info_by_id(card_info_id: int, card_id: int, deck_id: int):
    return db.session.execute(
        db.select(CardInfo.id)
        .join(CardInfo.parent_card)
        .join(Card.parent_deck)
        .where(Card.id == card_id)
        .where(Card.deck_id == deck_id)
        .where(CardInfo.id == card_info_id)
    ).scalar_one_or_none()
