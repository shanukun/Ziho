from flask import Blueprint

bp = Blueprint('main', __name__)

from ziho.main import routes
