from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import Length

from ziho.core.models import MAX_SIZE_DECK_NAME
from ziho.utils.forms import ZihoForm


class SearchDeckForm(ZihoForm):
    search_query = TextAreaField(
        "Search", validators=[Length(min=1, max=MAX_SIZE_DECK_NAME)]
    )
    tag = SelectField("Tags", coerce=int)
    submit = SubmitField("Search")

    def add_choices(self, tags):
        choices = [(0, "---")]
        choices.extend([(tag.id, tag.name) for tag in tags])
        self.tag.choices = choices
