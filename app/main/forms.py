from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import Required
from ..models import User


class ArticleForm(FlaskForm):

    title = StringField('Article title', validators=[Required()])
    post = TextAreaField('Article Post', validators=[Required()])
    submit = SubmitField('Submit')
