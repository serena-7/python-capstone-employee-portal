from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
Migrate(app, db)

from company_site.bp.main.views import main_bp  # NOQA

app.register_blueprint(main_bp, url_prefix="")
