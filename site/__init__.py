from site.bp.main.views import main_bp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import flask_migrate

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
Migrate(app, db)


app.register_blueprint(main_bp, url_prefix="")
