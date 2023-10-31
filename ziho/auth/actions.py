from typing import Any

from ziho import db
from ziho.models import User


def get_user_by_username(username: str) -> User | None:
    return db.session.execute(
        db.select(User).filter_by(username=username)
    ).scalar_one_or_none()


def get_user_by_email(email: str) -> User | None:
    return db.session.execute(
        db.select(User).filter_by(email=email)
    ).scalar_one_or_none()


def get_user_or_404(username: str) -> Any:
    return db.one_or_404(db.select(User).filter_by(username=username))


def create_user(username: str, email: str, password: str):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user.id
