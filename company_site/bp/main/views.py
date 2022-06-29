from flask import Blueprint, render_template, redirect, url_for
from company_site import db

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route("/")
def home():
    return render_template('home.html')
