from flask_wtf import FlaskForm
from wtforms import StringField , EmailField  , PasswordField, SubmitField , ValidationError
from wtforms.validators import  DataRequired , EqualTo , Length ,Email

from .models import User




class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist, try a different username')
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('Email already exist, try a different email')

    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = EmailField('Your Email', validators=[DataRequired(), Email() ])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1')])
    submit = SubmitField('Sign-Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

