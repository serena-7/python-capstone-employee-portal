from company_site import db
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard_bp.route("")
@login_required
def dashboard():
    return render_template('dashboard.html')
