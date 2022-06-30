from collections import namedtuple
from datetime import datetime, date, timedelta
from company_site.models import Jobcode
from company_site.bp.portal.timecards.forms import WEEKDAYS
from decimal import Decimal


def get_view_dates(start_date):
    view_dates = {}
    d = start_date
    for day in WEEKDAYS:
        view_dates[day] = d
        d += timedelta(days=1)

    return view_dates


def get_timecard_data(timecards, view_dates):
    groupings = {}
    default = Decimal(0.00)
    daily_totals = {'sun': default, 'mon': default, 'tue': default,
                    'wed': default, 'thr': default, 'fri': default, 'sat': default, 'total': default}
    is_locked = False

    for timecard in timecards:
        if timecard.locked == True:
            is_locked = True
        jobcode = Jobcode.query.get(timecard.jobcode_id)
        if timecard.code not in groupings:
            groupings[timecard.code] = {'jobcode': jobcode,
                                        'sun': None, 'mon': None, 'tue': None, 'wed': None, 'thr': None, 'fri': None, 'sat': None, 'total': 0}
        for key, value in view_dates.items():
            if value == timecard.date:
                groupings[timecard.code][key] = timecard.hours
                groupings[timecard.code]['total'] += timecard.hours
                daily_totals[key] += timecard.hours
                daily_totals['total'] += timecard.hours

    timeset = namedtuple(
        'timeset', ['jobcode', 'sun', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat', 'total'])

    data = {
        'timeset': []
    }

    totals = []

    for group in groupings.values():
        data['timeset'].append(timeset(group['jobcode'], group['sun'], group['mon'],
                               group['tue'], group['wed'], group['thr'], group['fri'], group['sat'], group['total']))

    return [data, daily_totals, is_locked]
