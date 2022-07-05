from company_site import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from company_site.models import User
from company_site.bp.admins.employees.forms import AddForm

admin_emp_bp = Blueprint('admin_emp', __name__, template_folder='templates')


@admin_emp_bp.route('/')
@login_required
def employees():
    admins = User.query.filter_by(
        active=True, admin=True).order_by('last_name').all()
    non_admins = User.query.filter_by(active=True, admin=False)
    past_employees = User.query.filter_by(
        active=False).order_by('last_name').all()
    return render_template('employee_list.html', admins=admins, non_admins=non_admins, past=past_employees)


@admin_emp_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = AddForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        admin = form.admin.data
        user = User(email=email, password=password, first_name=first_name,
                    last_name=last_name, phone_number=phone_number, admin=admin)
        db.session.add(user)
        db.session.commit()
        flash(f"Employee {user.last_name}, {user.first_name} Added", "success")
        return redirect(url_for('admin_emp.employees'))

    return render_template('add_employee.html', form=form)


@admin_emp_bp.route('/<user_id>')
@login_required
def employee_info(user_id):
    user = User.query.get(user_id)
    return render_template('employee_info.html', user=user)


@admin_emp_bp.route('/<user_id>/change_password')
@login_required
def change_password(user_id):
    user = User.query.get(user_id)
    form = ChangePasswordForm()
    pass


@admin_emp_bp.route('/<user_id>/activate')
@login_required
def activate(user_id):
    user = User.query.get(user_id)
    user.active = True
    db.session.commit()
    flash(f"{user.last_name}, {user.first_name} Activated", "success")
    return redirect(url_for('admin_emp.employees'))


@admin_emp_bp.route('/<user_id>/deactivate')
@login_required
def deactivate(user_id):
    user = User.query.get(user_id)
    user.active = False
    db.session.commit()
    flash(f"{user.last_name}, {user.first_name} Deactivated", "success")
    return redirect(url_for('admin_emp.employees'))
