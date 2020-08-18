from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(), Length(max=20, message="Max of 20 characters")])
    password = PasswordField("Password", validators=[InputRequired()])

class RegisterForm(LoginForm):

    email = StringField("Email", validators=[Email()])
    first_name = StringField("First Name", validators=[Length(max=30)])
    last_name = StringField("Last Name", validators=[Length(max=30)])