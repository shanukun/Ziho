class AjaxError(Exception):
    status_code = 400

    def __init__(self, messages, status_code=None, payload=None):
        super().__init__()
        self.messages = messages
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.messages
        return rv


class InvalidFormData(AjaxError):
    status_code = 406

    def __init__(self, errors_dict):
        errors = []
        for field_key in errors_dict:
            if field_key is not None:
                for msg in errors_dict[field_key]:
                    errors.append(f"{field_key.replace('_', ' ').capitalize()} {msg}")
        super().__init__(messages=errors)


class ServerError(AjaxError):
    status_code = 500
