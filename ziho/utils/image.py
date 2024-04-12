import os
import time

from flask import url_for
from werkzeug.utils import secure_filename

from ziho.utils.helper import generate_random_string


# TODO temp sol, use more robust approach for saving images
def save_image(app, image_data):
    ts = str(int(time.time()))
    ext = "." + image_data.filename.split(".")[-1]
    filename = secure_filename(generate_random_string() + ts + ext)
    full_path = os.path.join(app.config["UPLOAD_PATH"], filename)
    image_data.save(full_path)
    return url_for("home.show_image", image_name=filename, _external=True)


def get_image_path(app, image):
    image_path = None
    if image:
        image_path = save_image(app, image)
    return image_path
