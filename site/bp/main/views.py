from flask import Blueprint, render_template, redirect, url_for
from site import db

main_bp = Blueprint('main', __name__, template_folder='templates')
