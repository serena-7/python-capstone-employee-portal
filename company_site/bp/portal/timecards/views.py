from company_site import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import datetime, date, timedelta
from flask_login import current_user, login_required

from company_site.models import User, Jobcode, Timecard, PTO
from company_site.bp.portal.timecards.forms import TimecardRowForm, TimecardSetForm, WEEKDAYS
from company_site.bp.portal.timecards.helpers import get_timecard_data, get_view_dates

timecards_bp = Blueprint('timecards', __name__, template_folder='templates')


@timecards_bp.route('/<targ_date>', methods=['GET', 'POST'])
@login_required
def timecards(targ_date):
    # set start_date (sunday of week containing target date)
    if targ_date == 'current':
        today = date.today()
        start_date = today - timedelta(days=(today.weekday()+1) % 7)
    else:
        targ_date = datetime.strptime(targ_date, '%b-%d-%Y').date()
        start_date = targ_date - timedelta(days=(targ_date.weekday()+1) % 7)

    # create dictionary of actual dates for each weekday
    view_dates = get_view_dates(start_date)

    # get all user timecards within date range
    view_timecards = Timecard.query.join(Jobcode, Timecard.jobcode_id == Jobcode.jobcode_id).add_columns(Timecard.jobcode_id.label('jobcode_id'), Jobcode.code.label('code'), Timecard.date.label(
        'date'), Timecard.hours.label('hours'), Timecard.locked.label('locked')).filter((Timecard.user_id == current_user.user_id) & (Timecard.date >= view_dates['sun']) & (Timecard.date <= view_dates['sat'])).order_by(Timecard.date).all()

    # create data set and import existing values into form
    data, daily_totals, is_locked = get_timecard_data(
        view_timecards, view_dates)
    form = TimecardSetForm(data=data)

    if form.validate_on_submit():
        for row in form.timeset:  # loop through rows of table
            jobcode = row.jobcode.data
            if jobcode:  # if row has a jobcode proceed
                for field in row:  # loop through fields in row
                    # extract end of name from field
                    name = field.name.split('-')[2]
                    # check if data exists and if it is a time entry
                    if (field.data or field.data == 0) and name != 'jobcode' and name != 'total' and name != 'csrf_token':
                        field_date = view_dates[name]
                        # query database to see if timecard already exists
                        existing_timecard = Timecard.query.filter_by(
                            user_id=current_user.user_id, jobcode_id=jobcode.jobcode_id, date=field_date).first()
                        if existing_timecard:
                            # if timecard exists and data is 0 delete timecard
                            if field.data == 0:
                                db.session.delete(existing_timecard)
                            # else update timecard
                            else:
                                existing_timecard.hours = field.data
                        # if new entry and data is not 0 add new timecard
                        elif field.data != 0:
                            timecard = Timecard(
                                user_id=current_user.user_id, jobcode_id=jobcode.jobcode_id, date=field_date, hours=field.data, locked=False)
                            db.session.add(timecard)
        db.session.commit()
        # reload page with saved timecards
        return redirect(url_for('timecards.timecards', targ_date=view_dates['sun'].strftime('%b-%d-%Y')))

    return render_template('timecards.html', form=form, dates=view_dates, totals=daily_totals, is_locked=is_locked)


@timecards_bp.route('/<targ_date>/<direction>')
@login_required
def nav_view(targ_date, direction):
    # check direction to calculate the next date
    if direction == 'prev':
        targ_date = datetime.strptime(targ_date, '%b-%d-%Y').date()
        next_date = targ_date - timedelta(days=7)
    elif direction == 'next':
        targ_date = datetime.strptime(targ_date, '%b-%d-%Y').date()
        next_date = targ_date + timedelta(days=7)
    else:  # if error in direction type flash error and reload page at original target
        flash("Invalid request", "danger")
        return redirect(url_for('timecards.timecards', targ_date=targ_date))
    # turn date into string and input into url for timecards
    next_date = next_date.strftime('%b-%d-%Y')
    return redirect(url_for('timecards.timecards', targ_date=next_date))
