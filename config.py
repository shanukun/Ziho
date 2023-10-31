import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hardcoded-string"

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TESTING = False


class TestingConfig(Config):
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///"

    # Disable check for csrf token
    WTF_CSRF_ENABLED = False

    TESTING = True
