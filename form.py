from unicodedata import category
from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import (PasswordField, SelectField, StringField, SubmitField, TextAreaField, FileField)
from wtforms.validators import DataRequired, EqualTo


class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Uttarakhand History'), ('Uttarakhand Geography'),('Uttarakhand Current'),('India History'),('India Geography'),('India Current'),('Hindi'),('Computer')], validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Feature Photo')
    submit = SubmitField('Save Post')


class LoginForm(FlaskForm):
    email = StringField('Email-Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UserForm(FlaskForm):

    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone')
    about_author = TextAreaField('About')
    security_question = SelectField('Security Question',validators=[DataRequired()], choices=[('What is your favourite color?'), ('What is your favourite hobby?'),('What is your favourite food?')])
    security_answer = StringField('Security Answer',validators=[DataRequired()])
    password_hash=PasswordField('Password', validators=[DataRequired()])
    # password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
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

    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone = StringField('Phone')
    email = StringField('Email')
    about_author = StringField('About')
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