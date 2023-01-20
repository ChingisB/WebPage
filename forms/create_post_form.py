from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    title = StringField('Тема', validators=[DataRequired()])
    desc = StringField('Краткое описание', validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Создать')
