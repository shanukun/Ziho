from ziho import app, db
from ziho.models import Deck, User


@app.shell_context_processor
def make_shel_context():
    return {"db": db, "User": User, "Deck": Deck}
