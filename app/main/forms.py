from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import Required
from ..models import User


class ArticleForm(FlaskForm):
    title = StringField('Article title', validators=[Required()])
    post = TextAreaField('Article Post')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    username = StringField('Your Name', validators=[Required()])
    comment = TextAreaField('Your Comment', validators=[Required()])
    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')
