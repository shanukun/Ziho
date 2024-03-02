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
    decks: Mapped[List["Deck"]] = relationship(
        back_populates="creator", cascade="all, delete", passive_deletes=True
    )

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

    created_at: Mapped[datetime] = mapped_column(
        DateTime, index=True, default=datetime.utcnow
    )
    name: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )

    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    creator: Mapped["User"] = relationship(back_populates="decks")

    cards: Mapped[List["Card"]] = relationship(
        back_populates="parent_deck", cascade="all, delete", passive_deletes=True
    )

    def __repr__(self):
        return "<Deck {}>".format(self.name)


class Card(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    back: Mapped[str] = mapped_column(String(500))
    front: Mapped[str] = mapped_column(String(200), nullable=False)
    image_path: Mapped[str] = mapped_column(String(500), nullable=True)

    deck_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("deck.id", ondelete="CASCADE")
    )
    parent_deck: Mapped["Deck"] = relationship(back_populates="cards")
    card_info: Mapped["CardInfo"] = relationship(
        back_populates="parent_card", cascade="all, delete-orphan"
    )


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

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE")
    )
    card_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("card.id", ondelete="CASCADE")
    )
    parent_card: Mapped["Card"] = relationship(back_populates="card_info")
