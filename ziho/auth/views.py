from urllib.parse import urlparse

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from ziho.auth import bp
from ziho.auth.forms import LoginForm, RegistrationForm
from ziho.auth.handlers import create_user, get_user_by_username


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next = request.args.get("next")
        if not next or urlparse(next).netloc != "":
            next = url_for("main.home")
        return redirect(next)
    return render_template("auth/login.html", title="Login", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.email.data, form.password.data)
        flash("Congratulations, you are now a registered user!", "success")
        return redirect(url_for("auth.login"))
    flash(form.errors)
    return render_template("auth/register.html", title="Register", form=form)
