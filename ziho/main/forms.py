from flask_wtf import FlaskForm
from wtforms import (
    DateTimeField,
    FloatField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError

from ziho.auth.actions import get_user_by_username
from ziho.main.actions import get_card_info_by_id, get_deck_by_id


class DeckForm(FlaskForm):
    deck_name = StringField("Deck Name", validators=[DataRequired()])
    submit = SubmitField("Create Deck")




class GetCardReqForm(FlaskForm):
    class Meta:
        csrf = False

    deck_id = IntegerField("DeckId", validators=[DataRequired()])

    def validate_deck_id(self, deck_id):
        deck = get_deck_by_id(deck_id.data)
        if deck is None:
            raise ValidationError("Please use a valid deck id.")


class CardForm(FlaskForm):
    deck = SelectField("Deck", coerce=int)
    front = StringField("Front", validators=[DataRequired()])
    back = TextAreaField("Back", validators=[Length(min=1, max=500)])


class CardResponseForm(CardForm):
    deck = IntegerField("Deck")


class EditProfileForm(FlaskForm):
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
