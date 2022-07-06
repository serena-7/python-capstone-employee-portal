from company_site import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from company_site.models import User
from company_site.bp.portal.user.forms import LoginForm, ChangeEmailForm, ChangePasswordForm, ChangePhoneForm

user_bp = Blueprint('user', __name__, template_folder='templates')


@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")

            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Log in failed!")

    return render_template('login.html', form=form)


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('main.home'))


@user_bp.route("/account")
@login_required
def account():
    return render_template('account_info.html')


@user_bp.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.check_password(form.old_pass.data):
            current_user.update_password(form.password.data)
            db.session.commit()
            flash('Password updated', "success")
            logout_user()
            flash('Logged out! Please Login with new password.', 'warning')
            return redirect(url_for('user.account'))
        else:
            flash('Old Password was Incorrect!', 'danger')
            return redirect(url_for('user.change_password'))

    return render_template('change_password.html', form=form)


@user_bp.route("/change_email", methods=['GET', 'POST'])
@login_required
def change_email():
    form = ChangeEmailForm()

    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Email updated!', "success")
        return redirect(url_for('user.account'))

    return render_template('change_email.html', form=form)


@user_bp.route("/change_phone", methods=['GET', 'POST'])
@login_required
def change_phone():
    form = ChangePhoneForm()

    if form.validate_on_submit():
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        flash('Phone Number updated!', "success")
        return redirect(url_for('user.account'))

    return render_template('change_phone.html', form=form)
