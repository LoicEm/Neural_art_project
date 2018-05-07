import os, subprocess

from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory

from frontend.forms import build_style_form, upload_image_from_form
from backend.neural_transfer import neural_transform

app = Flask(__name__)
app.secret_key = "super secret key"

# Check the conditions in which it opens a new browser tab
distant_condition = ('FLASK_DISTANT' not in os.environ) or not (os.environ['FLASK_DISTANT'])
debug_condition = ('FLASK_DEBUG' not in os.environ) or not (os.environ['FLASK_DEBUG'])


if distant_condition and debug_condition : # If the app is not launched on a distant server
    subprocess.run(['xdg-open', 'http://127.0.0.1:5000/'])  # Open the correct adress in the default browser

@app.route('/data/<path:filename>')
def data_path(filename):
    return send_from_directory('../data', filename)


@app.route('/')
def index():
    return render_template("home.html")


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
    return render_template("display_style_gallery.html", images=style_pics, folder="style/")

@app.route('/results_gallery')
def show_results_gallery():
    pics = os.listdir("data/results")
    return render_template("display_style_gallery.html", images=pics, folder="results/")


@app.route('/uploaded_file/<string:filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    """Display an uploaded file"""
    if request.method == 'POST': # When a form is filled it sends a POST request

        # Make the separation between the two forms
        if request.form['submit'] == "Upload":  # Form to upload style image
            return upload_image_from_form(request, 'content')

        elif request.form['submit'] == "Transform": # Form to launch style transfer
            style_pic = request.form['images']
            transform_name = '+'.join(i.split('/')[-1].split('.')[0] for i in [style_pic, filename]) + '.jpg'
            transform_path = 'data/results/' + transform_name
            size_transform = min(512, int(request.form['size']))

            # Make the transformation
            neural_transform('data/content/' + filename, 'data/' + request.form['images'],
                             transform_path, content_size=size_transform, style_scale=float(request.form['scale']))
            return redirect(url_for('results', filename=transform_name))
    style_pics = os.listdir('data/style')
    styleform= build_style_form(style_pics, 'style/')
    return render_template("display_image.html", image_name=filename, styleform=styleform)

    # TODO : Put it nicely
    # TODO : Preselect a style picture when it was just uploaded
    # TODO : add image size


@app.route('/results/<string:filename>')
def results(filename):
    print('went there')
    return render_template("display_result.html", filename=filename)