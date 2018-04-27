from flask_wtf import FlaskForm
from wtforms import RadioField, FloatField


class SelectStyleForm(FlaskForm):
    scale = FloatField("Choose a style image scale", default=1.0)
    images = RadioField('Choose a style image.', choices=[]) # Choices are to be determined later


def build_style_form(paths, folder=''):
    """Build a SelectStyleForm with a list of path to the style images
        paths : paths to the style images
        folder :folder they are in"""
    form = SelectStyleForm()
    form.images.choices = [(folder + path, path) for path in paths]
    print(form.images.choices)
    for subfield in form.images:
        print(dir(subfield), subfield.__dict__)
    return form