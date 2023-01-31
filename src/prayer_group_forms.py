from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectMultipleField, SelectField, PasswordField, EmailField, TelField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class InviteForm(FlaskForm):
    invite = StringField("Invitation Code: ", validators=[InputRequired("Please enter your Invitaton Code.")])
    submit = SubmitField("Continue")

class SignupForm(FlaskForm):
    fname = StringField("First Name: ", validators=[InputRequired("Please enter your First Name.")])
    lname = StringField("Last Name: ", validators=[InputRequired("Please enter your Last Name.")])
    email = EmailField("Email Address: ", validators=[InputRequired("Please enter your Email.")])
    password = PasswordField("Password: ", validators=[InputRequired("Please enter your Password."), Length(min=8, max=256)])
    confirm = PasswordField("Confirm Password: ", validators=[InputRequired(), Length(min=8, max=256), EqualTo('password', message='Passwords must match.')])
    phone_num = TelField("Phone Number (Optional): ")
    home_address = StringField("Home Address (Optional): ")
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = EmailField("Email Address: ", validators=[InputRequired("Please enter your Email.")])
    password = PasswordField("Password: ", validators=[InputRequired("Please enter your Password."), Length(min=8, max=256)])
    submit = SubmitField("Login")

class GroupForm(FlaskForm):
    name = StringField("Name: ", validators=[InputRequired("Please name the group.")])
    members = SelectMultipleField("Members: ", choices=[])

    submit = SubmitField("submit")

class GuidedForm(FlaskForm):
    category = StringField("Category: ", validators=[InputRequired("Please enter the category.")])
    reference = StringField("reference: ", validators=[InputRequired("Please enter the verse.")])
    text = StringField("Category: ", validators=[InputRequired("Please enter in the verse's text.")])

    submit = SubmitField("submit")