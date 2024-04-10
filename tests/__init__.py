from ziho import db


def setup_db(app):
    with app.app_context():
        db.create_all()


def teardown_db(app):
    """Destroy database."""

    with app.app_context():
        db.session.remove()
        db.drop_all()


def clean_db(app):
    """Clean all database data."""

    with app.app_context():
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
