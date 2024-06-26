from flask_login import current_user
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from ziho.auth.handlers import get_user_by_username
from ziho.utils.forms import ZihoForm


class ChangePasswordForm(ZihoForm):
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Password (again)", validators=[DataRequired(), EqualTo("password")]
    )

    def validate_old_password(self, old_password):
        user = get_user_by_username(current_user.username)
        if not user.check_password(old_password.data):
            raise ValidationError("Incorrent old password.")

    submit = SubmitField("Change Password")


class EditProfileForm(ZihoForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=440)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = get_user_by_username(username.data)
            if user is not None:
                raise ValidationError("Please use a different username.")
