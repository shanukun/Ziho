from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    DateTimeField,
    FileField,
    FloatField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError

from ziho.auth.handlers import get_user_by_username
from ziho.core.handler import get_deck_by_id, get_card_info_by_id


class ZihoForm(FlaskForm):
    def get_data(self, **kwargs):
        data = self.data
        data.pop("csrf_token", None)
        data.pop("submit", None)
        if kwargs:
            data.update(kwargs)
        return data


class DeckForm(ZihoForm):
    deck_name = TextAreaField("Deck Name", validators=[DataRequired()])
    submit = SubmitField("Create")

    def filter_deck_name(self, field):
        if field:
            return field.strip()


class DeckDeleteForm(ZihoForm):
    deck_id = IntegerField("deck_id", validators=[DataRequired()])
    submit = SubmitField("Delete")


class CardInfoForm(ZihoForm):
    deck_id = IntegerField("deck_id", validators=[DataRequired()])
    card_id = IntegerField("card_id", validators=[DataRequired()])
    card_info_id = IntegerField("card_info_id", validators=[DataRequired()])

    difficulty = FloatField("difficulty", validators=[InputRequired()])
    due = DateTimeField(
        "due", validators=[InputRequired()], format="%Y-%m-%dT%H:%M:%S.%f%z"
    )
    elapsed_days = FloatField("elapsed_days", validators=[InputRequired()])
    lapses = IntegerField("lapses", validators=[InputRequired()])
    last_review = DateTimeField(
        "last_review", validators=[InputRequired()], format="%Y-%m-%dT%H:%M:%S.%f%z"
    )
    reps = IntegerField("reps", validators=[InputRequired()])
    scheduled_days = IntegerField("scheduled_days", validators=[InputRequired()])
    stability = FloatField("stability", validators=[InputRequired()])
    state = IntegerField("state", validators=[InputRequired()])

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self, extra_validators)
        if not rv:
            return False
        card_info = get_card_info_by_id(
            self.card_info_id.data, self.card_id.data, self.deck_id.data
        )
        print("[card info]: ", card_info)
        if card_info is None:
            raise ValidationError("Please use a valid card id.")
        return True


# TODO check if user is author of deck.
class GetCardsRequestForm(ZihoForm):
    deck_id = IntegerField("DeckId", validators=[DataRequired()])

    def validate_deck_id(self, deck_id):
        deck = get_deck_by_id(deck_id.data)
        if deck is None:
            raise ValidationError("Please use a valid deck id.")


IMAGES = "jpg jpe jpeg png gif svg bmp webp".split()


class CardForm(ZihoForm):
    deck_id = SelectField("Deck", coerce=int)
    front = TextAreaField("Front", validators=[DataRequired()])
    back = TextAreaField("Back", validators=[DataRequired()])
    card_image = FileField(
        "Card Image",
        validators=[
            FileAllowed(
                IMAGES,
                message=f"Image extensions which are allowed: {(', ').join(IMAGES)}",
            ),
        ],
    )
    submit = SubmitField("Add Card")


class AddCardForm(CardForm):
    def add_choices(self, decks):
        self.deck_id.choices = [(deck.id, deck.name) for deck in decks]


class CardCreationForm(CardForm):
    deck_id = IntegerField("Deck", validators=[DataRequired()])


class CardUpdateForm(CardCreationForm):
    card_id = IntegerField("Card", validators=[DataRequired()])
    submit = SubmitField("Update Card")

    def validate_card_id(self, card_id):
        pass


class CardDeleteForm(ZihoForm):
    deck_id = IntegerField("Deck", validators=[DataRequired()])
    card_id = IntegerField("Card", validators=[DataRequired()])
    submit = SubmitField("Delete")


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
