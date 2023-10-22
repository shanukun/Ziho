from flask import Blueprint

bp = Blueprint('errors', __name__)


from ziho.errors import handlers
