from flask import render_template, jsonify

from ziho import db
from ziho.errors import bp
from ziho.errors.errors import AjaxError


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500


@bp.app_errorhandler(AjaxError)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code
