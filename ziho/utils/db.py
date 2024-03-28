from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ziho.core.exceptions import PersistenceError


def try_commit(session, msg):
    try:
        session.commit()
    except IntegrityError:
        raise PersistenceError("Entity already exists.")
    except SQLAlchemyError:
        raise PersistenceError(msg)
