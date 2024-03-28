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


class ServerError(AjaxError):
    status_code = 500
