from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, Optional, EqualTo

from company_site.models import User


class AddForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[
                                 InputRequired("Input Required"),
                                 DataRequired("Data Required")
                             ])
    last_name = StringField('Last Name',
                            validators=[
                                InputRequired("Input Required"),
                                DataRequired("Data Required")
                            ])
    email = StringField('Email',
                        validators=[
                            InputRequired("Input Required"),
                            DataRequired("Data Required")
                        ])
    phone_number = StringField('Phone Number',
                               validators=[
                                   Optional(),
                                   Length(min=10, max=10,
                                          message="Must be 10 digits long")
                               ])
    password = PasswordField('Password',
                             validators=[
                                 InputRequired("Input Required"),
                                 Length(min=6, max=20,
                                        message="Must be 6 to 20 characters."),
                                 EqualTo("conf_pass",
                                         message="Password must match!")
                             ])
    conf_pass = PasswordField('Confirm Password',
                              validators=[
                                  InputRequired("Input Required")
                              ])
    admin = BooleanField('Admin Privledges')
    submit = SubmitField('Add Employee')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError("Email already has account!")

    def validate_phone_number(self, phone_number):
        if not self.phone_number.data.isdigit():
            raise ValidationError("Phone Number must contain numbers only.")


class EditForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[
                                 InputRequired("Input Required"),
                                 DataRequired("Data Required")
                             ])
    last_name = StringField('Last Name',
                            validators=[
                                InputRequired("Input Required"),
                                DataRequired("Data Required")
                            ])
    phone_number = StringField('Phone Number',
                               validators=[
                                   Optional(),
                                   Length(min=10, max=10,
                                          message="Must be 10 digits long")
                               ])
    submit = SubmitField('Update Info')

    def validate_phone_number(self, phone_number):
        if not self.phone_number.data.isdigit():
            raise ValidationError("Phone Number must contain numbers only.")


class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password',
                             validators=[
                                 InputRequired("Input Required"),
                                 Length(min=6, max=20,
                                        message="Must be 6 to 20 characters."),
                                 EqualTo("conf_pass",
                                         message="Password must match!")
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
