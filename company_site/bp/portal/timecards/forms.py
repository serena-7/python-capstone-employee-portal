from flask_wtf import FlaskForm
from wtforms import FormField, FieldList
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, DateField, DecimalField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange, ValidationError, Optional
from datetime import datetime, date, timedelta

from company_site.models import User, Jobcode, Timecard, PTO

WEEKDAYS = ['sun', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat']


def active_jobcodes():
    return Jobcode.query.filter_by(active=True).all()


class TimecardRowForm(FlaskForm):
    jobcode = QuerySelectField(
        "Jobcode", query_factory=active_jobcodes, get_label='code', allow_blank=True)
    sun = DecimalField('hours', places=2, validators=[Optional(),
                                                      NumberRange(min=0, max=24, message="Hours must be between 0 and 24")])
    mon = DecimalField('hours', places=2, validators=[Optional(),
                                                      NumberRange(min=0, max=24, message="Hours must be between 0 and 24")])
    tue = DecimalField('hours', places=2, validators=[Optional(),
                                                      NumberRange(min=0, max=24, message="Hours must be between 0 and 24")])
    wed = DecimalField('hours', places=2, validators=[Optional(),
                                                      NumberRange(min=0, max=24, message="Hours must be between 0 and 24")])
    thr = DecimalField('hours', places=2, validators=[Optional(),
                                                      NumberRange(min=0, max=24, message="Hours must be between 0 and 24")])
    fri = DecimalField('hours', places=2, validators=[Optional(),
                                                      NumberRange(min=0, max=24, message="Hours must be between 0 and 24")])
    sat = DecimalField('hours', places=2, validators=[Optional(),
                                                      NumberRange(min=0, max=24, message="Hours must be between 0 and 24")])
    total = DecimalField('total', places=2, validators=[Optional()])


class TimecardSetForm(FlaskForm):
    timeset = FieldList(FormField(TimecardRowForm), min_entries=10)
    submit = SubmitField("Submit Time Entries")
