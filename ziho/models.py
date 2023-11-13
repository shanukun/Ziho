from datetime import datetime
from hashlib import md5
from typing import List

from flask_login import UserMixin
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from ziho import db, login_manager


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    about_me: Mapped[str] = mapped_column(String(140), nullable=True)
    decks: Mapped[List["Deck"]] = relationship(back_populates="creator", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )


@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()


class Deck(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, index=True, default=datetime.utcnow
    )
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped["User"] = relationship(back_populates="decks")
    parent_id: Mapped[int] = mapped_column(ForeignKey("deck.id"), nullable=True)
    cards: Mapped[List["Card"]] = relationship(
        back_populates="parent_deck", lazy="dynamic"
    )
    parent = relationship("Deck")

    def __repr__(self):
        return "<Deck {}>".format(self.name)


class Card(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    front: Mapped[str] = mapped_column(String(200), nullable=False)
    back: Mapped[str] = mapped_column(String(500))
    deck_id: Mapped[int] = mapped_column(ForeignKey("deck.id"))
    parent_deck: Mapped["Deck"] = relationship(back_populates="cards")
    card_info: Mapped["CardInfo"] = relationship(back_populates="parent_card")


class CardInfo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    difficulty: Mapped[float] = mapped_column(Float, default=0)
    due: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    elapsed_days: Mapped[float] = mapped_column(Float, default=0)
    lapses: Mapped[int] = mapped_column(Integer, default=0)
    last_review: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    reps: Mapped[int] = mapped_column(Integer, default=0)
    scheduled_days: Mapped[int] = mapped_column(Integer, default=0)
    stability: Mapped[float] = mapped_column(Float, default=0)
    state: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    card_id: Mapped[int] = mapped_column(ForeignKey("card.id"))
    parent_card: Mapped["Card"] = relationship(back_populates="card_info")
