from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, FileField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Optional

EARLIEST_YEAR = 1888
CURRENT_YEAR = 2020

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(), Length(max=20, message="Max of 20 characters")])
    password = PasswordField("Password", validators=[InputRequired()])

class RegisterForm(LoginForm):

    email = StringField("Email", validators=[Email()])
    first_name = StringField("First Name", validators=[Length(max=30)])
    last_name = StringField("Last Name", validators=[Length(max=30)])

class CardForm(FlaskForm):

    player = StringField("Player", validators=[InputRequired()])
    year = SelectField("Year", choices=[(year, year) for year in reversed(range(EARLIEST_YEAR, CURRENT_YEAR + 1))], validators=[Optional()])
    set_name = StringField("Set", validators=[InputRequired()])
    number = StringField("Number")
    parallel = BooleanField("Parallel")
    img = FileField("Upload Image", validators=[Optional()])