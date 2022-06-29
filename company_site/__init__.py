from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
Migrate(app, db)

from company_site.bp.main.views import main_bp  # NOQA
from company_site.bp.portal.user.views import user_bp  # NOQA
from company_site.bp.portal.dashboard.views import dashboard_bp  # NOQA


app.register_blueprint(main_bp, url_prefix="")
app.register_blueprint(user_bp, url_prefix="/portal/user")
app.register_blueprint(dashboard_bp, url_prefix="/portal/dashboard")

login_manager.init_app(app)
login_manager.login_view = "user.login"