from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

from ocr_engine import extract_text_and_overlay

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# HOME PAGE
@app.route("/")
def index():

    return render_template("index.html")


# IMAGE OCR
@app.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return "No image uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No selected file"

    filename = secure_filename(file.filename)

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(image_path)

    extracted_text, processed_image = \
        extract_text_and_overlay(image_path)

    return render_template(
        "index.html",
        extracted_text=extracted_text,
        image_file=filename,
        processed_image=processed_image
    )


if __name__ == "__main__":

    app.run(debug=True)