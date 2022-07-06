from company_site import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from company_site.models import User
from company_site.bp.admins.employees.forms import AddForm, EditForm, ChangePasswordForm, ChangeEmailForm

admin_emp_bp = Blueprint('admin_emp', __name__, template_folder='templates')


@admin_emp_bp.route('/')
@login_required
def employees():
    admins = User.query.filter_by(
        active=True, admin=True).order_by('last_name').all()
    non_admins = User.query.filter_by(
        active=True, admin=False).order_by('last_name').all()
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
    return render_template('employee_info.html', employee=user)


@admin_emp_bp.route('/<user_id>/edit_info', methods=['GET', 'POST'])
@login_required
def edit_info(user_id):
    user = User.query.get(user_id)
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': user.phone_number
    }
    form = EditForm(data=data)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone_number = form.phone_number.data
        db.session.commit()
        flash(
            f"Info updated for {user.last_name}. {user.first_name}", "success")
        return redirect(url_for('admin_emp.employee_info', user_id=user.user_id))

    return render_template('admin_edit_info.html', form=form, employee=user)


@admin_emp_bp.route('/<user_id>/change_password', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    user = User.query.get(user_id)
    form = ChangePasswordForm()

    if form.validate_on_submit():
        password = form.password.data
        user.update_password(password)
        db.session.commit()
        flash(
            f"Password changed for {user.last_name}, {user.first_name}", "success")
        return redirect(url_for('admin_emp.employees'))
    return render_template('admin_change_password.html', form=form, employee=user)


@admin_emp_bp.route('/<user_id>/change_email', methods=['GET', 'POST'])
@login_required
def change_email(user_id):
    user = User.query.get(user_id)
    form = ChangeEmailForm()

    if form.validate_on_submit():
        email = form.email.data
        user.email = email
        db.session.commit()
        flash(
            f"Email changed for {user.last_name}, {user.first_name}", "success")
        return redirect(url_for('admin_emp.employee_info', user_id=user.user_id))

    return render_template('admin_change_email.html', form=form, employee=user)


@admin_emp_bp.route('/<user_id>/activate')
@login_required
def activate(user_id):
    if int(user_id) == current_user.user_id:
        flash('Cannot change your own activation status', 'danger')
    else:
        user = User.query.get(user_id)
        user.active = True
        db.session.commit()
        flash(f"{user.last_name}, {user.first_name} Activated", "success")
    return redirect(url_for('admin_emp.employees'))


@admin_emp_bp.route('/<user_id>/deactivate')
@login_required
def deactivate(user_id):
    if int(user_id) == current_user.user_id:
        flash('Cannot change your own activation status', 'danger')
    else:
        user = User.query.get(user_id)
        user.active = False
        db.session.commit()
        flash(f"{user.last_name}, {user.first_name} Deactivated", "success")
    return redirect(url_for('admin_emp.employees'))


@admin_emp_bp.route('/<user_id>/invoke_admin')
@login_required
def invoke_admin(user_id):
    if int(user_id) == current_user.user_id:
        flash('Cannot change your own admin status', 'danger')
    else:
        user = User.query.get(user_id)
        user.admin = True
        db.session.commit()
        flash(f"Added Admin: {user.last_name}, {user.first_name}", "success")
    return redirect(url_for('admin_emp.employees'))


@admin_emp_bp.route('/<user_id>/revoke_admin')
@login_required
def revoke_admin(user_id):
    if int(user_id) == current_user.user_id:
        flash('Cannot change your own admin status', 'danger')
    else:
        user = User.query.get(user_id)
        user.admin = False
        db.session.commit()
        flash(f"Removed Admin: {user.last_name}, {user.first_name}")
    return redirect(url_for('admin_emp.employees'))
