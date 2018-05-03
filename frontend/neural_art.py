from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
import os
from frontend.forms import build_style_form, upload_image_from_form

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/data/<path:filename>')
def data_path(filename):
    return send_from_directory('../data', filename)


@app.route('/')
def index():
    return render_template("base.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return upload_image_from_form(request, 'content', 'uploaded')
    # check if the post request has the file part
    return render_template("upload_content.html")


@app.route('/content_gallery')
def show_content_gallery():
    content_pics = os.listdir('data/content')
    return render_template("display_content_gallery.html", images=content_pics)


@app.route('/style_gallery', methods=['GET', 'POST'])
def show_style_gallery():
    if request.method == 'POST':
        return upload_image_from_form(request, 'style')
    style_pics = os.listdir("data/style")
    return render_template("display_style_gallery.html", images=style_pics)


@app.route('/uploaded_file/<string:filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    """Display an uploaded file"""
    if request.method == 'POST':
        # Make the separation between the two forms
        if request.form['submit'] == "Upload":  # Form to upload style image
            return upload_image_from_form(request, 'content')
        elif request.form['submit'] == "Transform":
            redirect()
    style_pics = os.listdir('data/style')
    styleform= build_style_form(style_pics, 'style/')
    return render_template("display_image.html", image_name=filename, styleform=styleform)

    # TODO : Put it nicely
    # TODO : Preselect a style picture when it was just uploaded
    # TODO : add image size


@app.route('/results/<string:filename>')
def mixed_file():

    # TODO : add a "loading" button ? Or an interstitial page
    pass