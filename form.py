from unicodedata import category
from wsgiref import validate

from flask_wtf import FlaskForm
from wtforms import (PasswordField, SelectField, StringField, SubmitField,
                     TextAreaField, FileField)
from wtforms.validators import DataRequired, EqualTo


class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Uttarakhand History'), ('Uttarakhand Geography'),('Uttarakhand Current'),('India History'),('India Geography'),('India Current'),('Hindi')], validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Post')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UserForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    about_author = TextAreaField('About', validators=[DataRequired()])
    security_question = SelectField('Security Question', choices=[('What is your favourite color?'), ('What is your favourite hobby?'),('What is your favourite food?')], validators=[DataRequired()])
    security_answer = StringField('Security Answer', validators=[DataRequired()])
    password_hash=PasswordField('Password', validators=[DataRequired(),EqualTo('password_hash2',message='Passwords Must Match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class roleForm(FlaskForm):
    role=SelectField('Role', choices=[('Admin'), ('User'),('Author')], validators=[DataRequired()])
    submit = SubmitField('Set Role')


class ContactForm(FlaskForm):
    yourname = StringField('Your Name', validators=[DataRequired()])
    youremail = StringField('Your Email', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')


class editProfileForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    about_author = StringField('About', validators=[DataRequired()])
    profile_pic=FileField('Profile Picture')
    submit = SubmitField('Save Changes')



class forgotPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Submit')

class resetPassword(FlaskForm):
    security_question= SelectField('Security Question', choices=[('What is your favourite color?'), ('What is your favourite hobby?'),('What is your favourite food?')], validators=[DataRequired()])
    security_answer = StringField('Security Answer', validators=[DataRequired()])
    password_hash=PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')