from urllib.parse import urlparse

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ziho import db
from ziho.main import bp
from ziho.main.forms import EditProfileForm
from ziho.models import User


@bp.route("/")
@bp.route("/home")
@login_required
def home():
    decks = [
        {"user": {"username": "John"}, "name": "Operating System"},
        {"user": {"username": "Susan"}, "name": "System Design"},
    ]
    return render_template("home.html", title="Home", decks=decks)


@bp.route("/user/<username>")
@login_required
def user(username):
    user = db.one_or_404(db.select(User).filter_by(username=username))
    decks = [
        {"user": user, "name": "Operating System"},
        {"user": user, "name": "System Design"},
    ]
    return render_template("user.html", user=user, decks=decks)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

