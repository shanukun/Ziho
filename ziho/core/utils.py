from ziho.core.exceptions import PersistenceError
from ziho.errors.errors import InvalidFormData, ServerError
from ziho.utils.helper import get_rendered_form, get_response, get_response_form


class FormPost:
    """
    For handling form submitions.
    """

    def __init__(self, handler, form, form_template, form_name, success_message):
        self.handler = handler
        self.form = form
        self.form_template = form_template
        self.form_name = form_name
        self.success_message = success_message

    def do_post(self):
        if self.form.validate_on_submit():
            try:
                self.handler()
            except PersistenceError as e:
                raise ServerError(get_response(message=e.message))
            return get_response_form(
                message=self.success_message,
                rendered_form=self.rendered_form(),
                success=True,
            )
        else:
            raise InvalidFormData(
                get_response_form(
                    message="Invalid form.",
                    rendered_form=self.rendered_form(),
                )
            )

    def rendered_form(self, **kwargs):
        return get_rendered_form(
            self.form, self.form_name, self.form_template, **kwargs
        )
