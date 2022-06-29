from company_site import db
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user

from company_site.models import User
from company_site.bp.portal.user.forms import LoginForm

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
