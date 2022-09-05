from flask_wtf import FlaskForm
from wtforms import StringField , EmailField  , PasswordField, SubmitField , ValidationError
from wtforms.validators import  DataRequired , EqualTo , Length ,Email
from flask_login import login_user , logout_user , login_required , current_user


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
    email = EmailField('Your Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[EqualTo('password1')])
    submit = SubmitField('Sign-Up')
#I NEED TO INSTALL EMAIL email_validation for EMAIL VALIDATION SUPPORT
#I NEED TO INSTALL EMAIL email_validation for EMAIL VALIDATION SUPPORT
#I NEED TO INSTALL EMAIL email_validation for EMAIL VALIDATION SUPPORT   check_password

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UserForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user and user.username != current_user.username :
            raise ValidationError('Username already exist, try a different username')
        
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user and user.email != current_user.email :
            raise ValidationError('Email already exist, try a different email')
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    email = EmailField('Your Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Update')

class PasswordChangeForm(FlaskForm):

    def validate_old_password(self, old_password):
        user = User.query.filter_by(username = current_user.username ).first()
        if user and user.check_password(old_password):
            return True
        raise ValidationError('Old password did not match')
    old_password = PasswordField('Current password' , validators=[DataRequired()])
    new_password = PasswordField('Current password' , validators=[DataRequired(), Length(min=3)])
    confirm_password = PasswordField('Current password' , validators=[EqualTo('password1')])
    submit = SubmitField('Update password')