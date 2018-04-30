from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ProfileForm(FlaskForm):
    username = StringField('First Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    bio = TextAreaField('Biography', validators=[InputRequired()])
    photo= FileField('Profile Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg','png','Images Only!'])
    ])
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class PostForm(FlaskForm):
    photo=FileField('Photo', validators=[FileRequired('Please input a file'), FileAllowed(['jpg', 'png'], 'Images only!')])
    caption=StringField('Caption',validators=[InputRequired(message='Caption is required')])