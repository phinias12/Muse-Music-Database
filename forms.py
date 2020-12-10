from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    firstName = StringField('firstName', validators=[InputRequired(), Length(min=2, max=25)])
    lastName = StringField('lastName', validators=[InputRequired(), Length(min=2, max=50)])
    dob = DateField('dob', validators=[InputRequired()])

class SearchForm(FlaskForm):
    search = StringField('search')