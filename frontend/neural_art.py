from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from frontend.forms import build_style_form

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/data/<path:filename>')
def data_path(filename):
    return send_from_directory('data', filename)


@app.route('/')
def index():
    return render_template("base.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join("data/content/", filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("upload_content.html")



@app.route('/uploaded_file/<string:filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    """Display an uploaded file"""
    print("load", request.method)
    if request.method == 'POST':
        print(request.form)
        if "file" not in request.files:
            flash("No file selected for upload")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
        if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join("data/style/", filename))
                return redirect(request.url)

    style_pics = os.listdir('data/style')
    styleform= build_style_form(style_pics, 'style/')
    return render_template("display_image.html", image_name=filename, styleform=styleform)

#
# TODO : add option to upload your own style pic
# TODO :


@app.route('/result')
def mixed_file():
    pass