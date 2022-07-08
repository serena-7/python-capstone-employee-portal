from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# setup login manager, flask app, and database
login_manager = LoginManager()

app = Flask(__name__)

app.config.from_object('config')  # setup config variables from config.py

db = SQLAlchemy(app)
Migrate(app, db)

# get blueprints
from company_site.bp.main.views import main_bp  # NOQA
from company_site.bp.portal.user.views import user_bp  # NOQA
from company_site.bp.portal.dashboard.views import dashboard_bp  # NOQA
from company_site.bp.portal.timecards.views import timecards_bp  # NOQA
from company_site.bp.admins.employees.views import admin_emp_bp  # NOQA
from company_site.bp.admins.jobcodes.views import admin_jobcode_bp  # NOQA
from company_site.bp.admins.timecards.views import admin_timecard_bp  # NOQA

# register blueprints
app.register_blueprint(main_bp, url_prefix="")
app.register_blueprint(user_bp, url_prefix="/portal/user")
app.register_blueprint(dashboard_bp, url_prefix="/portal/dashboard")
app.register_blueprint(timecards_bp, url_prefix="/portal/timecards")
app.register_blueprint(admin_emp_bp, url_prefix="/admin/employees")
app.register_blueprint(admin_jobcode_bp, url_prefix="/admin/jobcodes")
app.register_blueprint(admin_timecard_bp, url_prefix="/admin/timecards")

# initialize login manager
login_manager.init_app(app)
# must come after blueprints are registered
login_manager.login_view = "user.login"
