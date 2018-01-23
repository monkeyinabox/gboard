from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from . import db
from .models import User

from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField(
        validators=[
            Email(),
            DataRequired(),
            Length(max=255)
        ]
    )
    password = PasswordField(
        validators=[
            DataRequired(),
            Length(max=255)])