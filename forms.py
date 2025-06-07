from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, URL, Length, Email, EqualTo

# Register form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Bookmark form
class BookmarkForm(FlaskForm):
    url = StringField('Bookmark URL', validators=[DataRequired(), URL()])
    description = StringField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('Work', 'Work'), ('Personal', 'Personal'), ('News', 'News')])
    submit = SubmitField('Save Bookmark')
