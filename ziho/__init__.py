import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import DeclarativeBase

from config import Config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    if config_class.DATABASE != "mysql":
        with app.app_context():

            @event.listens_for(db.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.session_protection = "strong"

    from ziho.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from ziho.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from ziho.home import bp as home_bp

    app.register_blueprint(home_bp)

    from ziho.deckview import bp as deckview_bp

    app.register_blueprint(deckview_bp)

    from ziho.explore import bp as explore_bp

    app.register_blueprint(explore_bp)

    from ziho.profile import bp as profile_bp

    app.register_blueprint(profile_bp)

    if not app.debug and not app.testing:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/ziho.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Ziho startup")

    return app
