from company_site import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from company_site.models import Jobcode
from company_site.bp.admins.jobcodes.forms import AddForm, EditForm

admin_jobcode_bp = Blueprint(
    'admin_jobcode', __name__, template_folder='templates')


@admin_jobcode_bp.route('/')
@login_required
def jobcodes():
    active_jobs = Jobcode.query.filter_by(active=True).all()
    inactive_jobs = Jobcode.query.filter_by(active=False).all()

    return render_template('jobcode_list.html', active=active_jobs, inactive=inactive_jobs)


@admin_jobcode_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_jobcode():
    form = AddForm()

    if form.validate_on_submit():
        code = form.code.data
        location = form.location.data
        jobcode = Jobcode(code=code, location=location)
        db.session.add(jobcode)
        db.session.commit()
        flash(f"Jobcode {jobcode.code} Added", "success")
        return redirect(url_for('admin_jobcode.jobcodes'))

    return render_template('add_jobcode.html', form=form)


@admin_jobcode_bp.route('/<jobcode_id>/edit', methods=['GET', 'POST'])
def edit_jobcode(jobcode_id):
    jobcode = Jobcode.query.get(jobcode_id)

    data = {
        'code': jobcode.code,
        'location': jobcode.location
    }

    form = EditForm(data=data)

    if form.validate_on_submit():
        jobcode.code = form.code.data
        jobcode.location = form.location.data
        db.session.commit()
        flash(f"{jobcode.code} Updated", "success")
        return redirect(url_for('admin_jobcode.jobcodes'))

    return render_template('edit_jobcode.html', form=form, jobcode=jobcode)


@admin_jobcode_bp.route('/<jobcode_id>/activate')
@login_required
def activate(jobcode_id):
    jobcode = Jobcode.query.get(jobcode_id)
    jobcode.active = True
    db.session.commit()
    flash(f"{jobcode.code} Activated", "success")
    return redirect(url_for('admin_jobcode.jobcodes'))


@admin_jobcode_bp.route('/<jobcode_id>/deactivate')
@login_required
def deactivate(jobcode_id):
    jobcode = Jobcode.query.get(jobcode_id)
    jobcode.active = False
    db.session.commit()
    flash(f"{jobcode.code} Deactivated", "success")
    return redirect(url_for('admin_jobcode.jobcodes'))
