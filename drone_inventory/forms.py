#outside of blueprint folder because it will be globally available within the drone_inventory project folder
#we are importing classes that need to be instantiated
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

#email, password, submit button
class UserLoginForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(), Email()])
    password = PasswordField('Password',validators = [DataRequired()])
    submit_button = SubmitField()