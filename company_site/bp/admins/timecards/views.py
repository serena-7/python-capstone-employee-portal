from company_site import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from company_site.models import User, Jobcode, Timecard

admin_timecard_bp = Blueprint(
    'admin_timecard', __name__, template_folder='templates')


@admin_timecard_bp.route('/')
@login_required
def timecard_home():
    return render_template('timecard_home.html')
