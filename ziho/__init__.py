from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from config import Config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

login_manager = LoginManager()
login_manager.login_view = "login"

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager.init_app(app)

migrate = Migrate(app, db)


from ziho import models, routes
