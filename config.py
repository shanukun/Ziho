import os
import sys
from pathlib import Path

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


def z_env(env_var: str) -> str | None:
    var_val = os.environ.get(env_var, None)
    return var_val


DATABASE_URL = "sqlite:///" + os.path.join(basedir, "app.db")
if os.environ.get("DATABASE") == "mysql":
    DATABASE_URL = f"mysql+pymysql://{z_env('MYSQL_USER')}:{z_env('MYSQL_PASS')}@{z_env('MYSQL_HOST')}:{z_env('MYSQL_PORT')}/{z_env('MYSQL_DB')}"


class Config:
    DATABASE = z_env("DATABASE")
    SECRET_KEY = z_env("SECRET_KEY") or "hardcoded-string"

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
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
