from flask import render_template


def get_rendered_form(form, form_name, template, **kwargs):
    context = {form_name: form}
    return render_template(template, **context, **kwargs)


def get_response(message=None, result=None):
    return {"message": message, "result": result}


def get_response_form(message=None, rendered_form=None):
    template_name = "error_template"
    return get_response(message, {template_name: rendered_form})


def get_handler_caller(func, *args, **kwargs):
    def handler_caller():
        return func(*args, **kwargs)

    return handler_caller
