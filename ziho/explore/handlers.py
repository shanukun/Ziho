from ziho import db
from ziho.core.exceptions import PersistenceError
from ziho.core.models import Card, CardInfo, Deck, Tag, User
from ziho.core.pagination import paginate
from ziho.utils.db import try_commit


def get_decks(page_no=1):
    stmt = (
        db.select(Deck, User)
        .join(Deck.creator)
        .join(Deck.cards)
        .group_by(Deck.id)
        .order_by(Deck.name)
    )

    pages = paginate(db, stmt, page=page_no, per_page=16)
    return pages


def clone_deck(user, form_data):
    original_deck = db.session.execute(
        db.select(Deck).where(Deck.id == form_data["deck_id"])
    ).scalar_one_or_none()
    if not original_deck:
        raise PersistenceError("Could not clone the deck.")

    deck = Deck(name=original_deck.name, creator_id=user.id)
    deck.tags.extend(original_deck.tags)
    db.session.add(deck)

    stmt = db.select(Card).where(Card.deck_id == original_deck.id)
    deck_cards = db.session.execute(stmt).all()
    if deck_cards:
        for (card,) in deck_cards:
            new_card = Card(
                front=card.front,
                back=card.back,
                image_path=card.image_path,
                parent_deck=deck,
            )
            card_info = CardInfo(parent_card=new_card, user_id=user.id)
            db.session.add(new_card)
            db.session.add(card_info)

    try_commit(db.session, f"Could not clone the deck: {original_deck.name}.")
    return deck.id
