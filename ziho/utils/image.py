import os

from flask import url_for
from werkzeug.utils import secure_filename


# TODO temp sol, use more robust approach for saving images
# Put in image utils
def save_image(app, image_data):
    filename = secure_filename(image_data.filename)
    full_path = os.path.join(app.config["UPLOAD_PATH"], filename)
    image_data.save(full_path)
    return url_for("home.show_image", image_name=filename, _external=True)


def get_image_path(app, image):
    image_path = None
    if image:
        image_path = save_image(app, image)
    return image_path
