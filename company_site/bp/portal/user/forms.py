from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, ValidationError
from flask_login import current_user

from company_site.models import User


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            InputRequired("Input is required"),
                            DataRequired("Data is required")
                        ])
    password = PasswordField("Password",
                             validators=[
                                 InputRequired("Input is required"),
                                 DataRequired("Data is required")
                             ])
    submit = SubmitField('Log In')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first() is None:
            raise ValidationError("Email is not registered!")


class ChangePasswordForm(FlaskForm):
    old_pass = PasswordField('Old Password',
                             validators=[
                                 InputRequired("Input Required")
                             ])
    password = PasswordField('New Password',
                             validators=[
                                 InputRequired("Input Required"),
                                 Length(min=6, max=20,
                                        message="Must be 6 to 20 characters."),
                                 EqualTo("conf_pass",
                                         message="Passwords must match!")
                             ])
    conf_pass = PasswordField('Confirm New Password',
                              validators=[
                                  InputRequired("Input Required")
                              ])
    submit = SubmitField('Change Password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email',
                        validators=[
                            InputRequired("Input Required"),
                            DataRequired("Data Required"),
                            EqualTo("conf_email", message="emails must match!")
                        ])
    conf_email = StringField('Confirm Email',
                             validators=[
                                 InputRequired("Input Required")
                             ])
    submit = SubmitField("Change Email")


class ChangePhoneForm(FlaskForm):
    phone_number = StringField('New Phone Number',
                               validators=[
                                   InputRequired("Input is Required"),
                                   DataRequired("Data is Required"),
                                   Length(min=10, max=10,
                                          message="Must be 10 digits long"),
                                   EqualTo("conf_phone",
                                           message="Phone Numbers Must Match!")
                               ])
    conf_phone = StringField('Confirm Phone Number',
                             validators=[
                                 InputRequired("Input is Required")
                             ])
    submit = SubmitField('Update Phone Number')

    def validate_phone_number(self, phone_number):
        if not self.phone_number.data.isdigit():
            raise ValidationError("Phone Number must contain numbers only.")
