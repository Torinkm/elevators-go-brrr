from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError # this imports a validator that checks data has been inputted


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min =1, max = 10, message = "Too many values")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')