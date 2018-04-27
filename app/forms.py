from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    gender = SelectField(label='Gender', choices=[("Male", "Male"), ("Female", "Female")])
    email = StringField('E-mail', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    bio = TextAreaField('Biography', validators=[InputRequired()])
    photo= FileField('Profile Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg','png','Images Only!'])
    ])