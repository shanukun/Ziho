from flask_wtf import FlaskForm
from wtforms import Field, TextAreaField
from wtforms.widgets import TextArea


class ZihoForm(FlaskForm):
    """
    Base form for all the ziho forms.
    """

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


class TagListField(Field):
    widget = TextArea()

    def _value(self):
        if self.data:
            return ", ".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip().lower() for x in valuelist[0].split(",")]
        else:
            self.data = []


class BetterTagListField(TagListField):
    def __init__(self, label=None, validators=None, remove_duplicates=True, **kwargs):
        super(BetterTagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(BetterTagListField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    def post_validate(self, form, validation_stopped):
        form.text_fields.append(self)

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates"""

        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item
