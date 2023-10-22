from ziho import create_app, db
from ziho.models import Deck, User

app = create_app()


@app.shell_context_processor
def make_shel_context():
    return {"db": db, "User": User, "Deck": Deck}
