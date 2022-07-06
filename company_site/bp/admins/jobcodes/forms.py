from flask_wtf import FlaskForm
from wtforms.fields import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, Optional

from company_site.models import User


class AddForm(FlaskForm):
    code = StringField('Jobcode Name',
                       validators=[
                           InputRequired("Input Required"),
                           DataRequired("Data Required")
                       ])
    location = StringField('Location',
                           validators=[
                               Optional()
                           ])
    submit = SubmitField('Add Jobcode')


class EditForm(FlaskForm):
    code = StringField('Jobcode Name',
                       validators=[
                           InputRequired("Input Required"),
                           DataRequired("Data Required")
                       ])
    location = StringField('Location',
                           validators=[
                               Optional()
                           ])
    submit = SubmitField('Edit Jobcode')
