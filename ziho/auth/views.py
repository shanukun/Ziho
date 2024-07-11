from urllib.parse import urlparse

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError

from ziho.auth import bp
from ziho.auth.forms import LoginForm, RegistrationForm
from ziho.auth.handlers import create_user, get_user_by_username
from ziho.core.exceptions import PersistenceError
from ziho.errors.errors import ServerError
from ziho.utils.helper import get_response


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = get_user_by_username(form.username.data)
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password.", "danger")
                return redirect(url_for("auth.login"))
        except SQLAlchemyError as e:
            raise ServerError(get_response(message=e._message))
        login_user(user, remember=form.remember_me.data)
        next = request.args.get("next")
        if not next or urlparse(next).netloc != "":
            next = url_for("home.home")
        return redirect(next)
    return render_template("auth/login.html", title="Login", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.home"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            create_user(form.username.data, form.email.data, form.password.data)
            flash("Congratulations, you are now a registered user!", "success")
            return redirect(url_for("auth.login"))
        except PersistenceError as e:
            flash("Could not register user.", "danger")
        return render_template("auth/register.html", title="Register", form=form)
    else:
        return render_template("auth/register.html", title="Register", form=form)
