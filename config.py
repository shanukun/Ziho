import os
from pathlib import Path

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


DATABASE = "sqlite:///" + os.path.join(basedir, "app.db")
if os.environ.get("DATABASE") == "mysql":
    pass


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hardcoded-string"

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = Path("ziho_uploads")
    UPLOAD_PATH = Path(basedir) / "ziho" / UPLOAD_FOLDER

    TESTING = False


class TestingConfig(Config):
    # in memory db
    SQLALCHEMY_DATABASE_URI = "sqlite:///"

    # Disable check for csrf token
    WTF_CSRF_ENABLED = False
    TESTING = True
