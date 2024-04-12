from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    BooleanField,
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
from ziho.core.handler import get_card_info_by_id, get_deck_by_id
from ziho.core.models import MAX_SIZE_BACK, MAX_SIZE_DECK_NAME, MAX_SIZE_FRONT


class ZihoForm(FlaskForm):
    def __init__(self, **kwargs):
        super(ZihoForm, self).__init__(**kwargs)
        self.text_fields = []

    def get_data(self, **kwargs):
        data = self.data
        data.pop("csrf_token", None)
        data.pop("submit", None)
        if kwargs:
            data.update(kwargs)
        return data

    def _clear_text_field(self):
        for tfields in self.text_fields:
            tfields.data = ""

    def validate(self, extra_validators=None):
        is_valid = super().validate(extra_validators)
        if is_valid:
            self._clear_text_field()
        return is_valid


class ZihoTextAreaField(TextAreaField):
    """
    Custom TextAreaField to clear field after successful validation.
    """

    def __init__(self, label=None, validators=None, **kwargs):
        super(ZihoTextAreaField, self).__init__(label, validators, **kwargs)

    def post_validate(self, form, validation_stopped):
        form.text_fields.append(self)


class DeckForm(ZihoForm):
    deck_name = ZihoTextAreaField(
        "Deck Name", validators=[DataRequired(), Length(min=1, max=MAX_SIZE_DECK_NAME)]
    )
    submit = SubmitField("Create")

    def filter_deck_name(self, field):
        if field:
            return field.strip()


class DeckDeleteForm(ZihoForm):
    deck_id = IntegerField("deck_id", validators=[DataRequired()])
    submit = SubmitField("Delete")


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"


class CardInfoForm(ZihoForm):
    deck_id = IntegerField("deck_id", validators=[DataRequired()])
    card_id = IntegerField("card_id", validators=[DataRequired()])
    card_info_id = IntegerField("card_info_id", validators=[DataRequired()])

    difficulty = FloatField("difficulty", validators=[InputRequired()])
    due = DateTimeField("due", validators=[InputRequired()], format=DATETIME_FORMAT)
    elapsed_days = FloatField("elapsed_days", validators=[InputRequired()])
    lapses = IntegerField("lapses", validators=[InputRequired()])
    last_review = DateTimeField(
        "last_review", validators=[InputRequired()], format=DATETIME_FORMAT
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
    front = ZihoTextAreaField(
        "Front", validators=[DataRequired(), Length(min=1, max=MAX_SIZE_FRONT)]
    )
    back = ZihoTextAreaField(
        "Back", validators=[DataRequired(), Length(min=1, max=MAX_SIZE_BACK)]
    )
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

    def set_select_default(self, value):
        self.deck_id.data = value

    def add_choices(self, decks):
        self.deck_id.choices = [(deck.id, deck.name) for deck in decks]


class CardUpdateForm(CardForm):
    deck_name = TextAreaField("Deck Name")
    deck_id = IntegerField("Deck", validators=[DataRequired()])
    card_id = IntegerField("Card", validators=[DataRequired()])
    front = TextAreaField(
        "Front", validators=[DataRequired(), Length(min=1, max=MAX_SIZE_FRONT)]
    )
    back = TextAreaField(
        "Back", validators=[DataRequired(), Length(min=1, max=MAX_SIZE_BACK)]
    )
    update_image = BooleanField(default=True)
    submit = SubmitField("Update Card")

    def set_deck_name(self, deck_name):
        self.deck_name.data = deck_name


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
