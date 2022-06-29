from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError

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
