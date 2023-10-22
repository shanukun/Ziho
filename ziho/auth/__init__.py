from flask import Blueprint

bp = Blueprint('auth', __name__)


from ziho.auth import routes
