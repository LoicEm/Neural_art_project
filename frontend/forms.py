from flask_wtf import FlaskForm
from wtforms import RadioField, FloatField, SubmitField
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
import os


class SelectStyleForm(FlaskForm):
    scale = FloatField("Choose a style image scale", default=1.0)
    images = RadioField('Choose a style image.', choices=[]) # Choices are to be determined later
    submit = SubmitField('Transform')


def build_style_form(paths, folder=''):
    """Build a SelectStyleForm with a list of path to the style images
        paths : paths to the style images
        folder :folder they are in"""
    form = SelectStyleForm()
    form.images.choices = [(folder + path, path) for path in paths]
    return form


def upload_image_from_form(request, type_image='style', redirect_url='same'):

    if redirect_url == 'same': # Redirects to the same url as the request
        redirect_url = request.url

    if "file" not in request.files:
        flash("No file selected for upload", 'error')
        print('no flash ?')
        return redirect(request.url)
    file = request.files["file"]

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        if redirect_url == 'uploaded':
            redirect_url = url_for('uploaded_file', filename=filename)
        file.save(os.path.join("data/" + type_image + '/', filename))
        return redirect(redirect_url)
