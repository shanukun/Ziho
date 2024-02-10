from ziho import db
from ziho.core.models import Card, CardInfo, Deck


def get_cards_for_deck(deck_id: int, type: str | None = None):
    stmt = db.select(Card).where(Card.deck_id == deck_id)
    cards = db.session.execute(stmt).all()
    if type == "dict":
        return {card.id: card for (card,) in cards}
    return [card for (card,) in cards]


def get_decks_by_user(user_id: int, type: str | None = None):
    decks_row = db.session.scalars(
        db.select(Deck).where(Deck.creator_id == user_id)
    ).all()
    if type == "dict":
        return {deck.id: deck for deck in decks_row}
    return [deck for deck in decks_row]


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
