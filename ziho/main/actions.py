from ziho import db
from ziho.models import Card, Deck


def create_deck(deck_name: str | None, user_id: int):
    deck = Deck(name=deck_name, creator_id=user_id)
    db.session.add(deck)
    db.session.commit()
    return deck.id


def get_decks_by_user(user_id: int):
    decks_row = db.session.execute(db.select(Deck).filter_by(creator_id=user_id)).all()
    return [deck for (deck,) in decks_row]


def create_card(deck_id: int, front: str, back: str):
    card = Card(front=front, back=back, deck_id=deck_id)
    db.session.add(card)
    db.session.commit()
    return card.id
