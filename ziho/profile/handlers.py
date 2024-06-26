from ziho import db
from ziho.auth.handlers import get_user_by_username
from ziho.core.models import Deck, User
from ziho.utils.db import try_commit


def change_password(user, form_data):
    user = get_user_by_username(user.username)
    user.set_password(form_data["password"])
    try_commit(db.session, "Could not change password.")


def update_profile(user, form_data):
    stmt = (
        db.update(User)
        .where(User.id == user.id)
        .values(username=form_data["username"], about_me=form_data["about_me"])
    )
    db.session.execute(stmt)

    try_commit(db.session, "Could not update profile.")


def get_decks_by_user(user_id: int, type: str | None = None):
    decks = db.session.execute(
        db.select(Deck).where(Deck.creator_id == user_id)
    ).scalars()
    if type == "dict":
        return {deck.id: deck for deck in decks}
    return [deck for deck in decks]
