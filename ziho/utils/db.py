from sqlalchemy.exc import SQLAlchemyError

from ziho.core.exceptions import PersistenceError


def try_commit(session, msg):
    try:
        session.commit()
    except SQLAlchemyError:
        raise PersistenceError(msg)
