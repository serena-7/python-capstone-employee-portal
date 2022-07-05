from company_site import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model):

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(10), nullable=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, email, password, first_name, last_name, phone_number=None, admin=None, active=None):
        self.email = email
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        if phone_number:
            self.phone_number = phone_number
        if admin:
            self.admin = admin
        if active:
            self.active = active

    # is_active, is_authenticated, is_anonymous, and get_id are required for flask-login
    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.user_id)
        except:
            raise "user_id can't be accessed"

    def check_password(self, given_password):
        return check_password_hash(self.password, given_password)

    def check_admin(self):
        return self.admin

    def update_password(self, password):
        self.password = generate_password_hash(password)


class Jobcode(db.Model):

    __tablename__ = 'jobcodes'
    jobcode_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(200), nullable=False, unique=True)
    location = db.Column(db.String(200), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, code, location=None, active=None):
        self.code = code
        if location:
            self.location = location
        if active:
            self.active = active


class Timecard(db.Model):

    __tablename__ = 'timecards'
    timecard_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.user_id"), nullable=False)
    jobcode_id = db.Column(db.Integer, db.ForeignKey(
        "jobcodes.jobcode_id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Numeric(3, 2), nullable=False)
    locked = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", backref=db.backref(
        "timecards", order_by=timecard_id))
    jobcode = db.relationship("Jobcode", backref=db.backref(
        "timecards", order_by=timecard_id))

    def __init__(self, user_id, jobcode_id, date, hours, locked=None):
        self.user_id = user_id
        self.jobcode_id = jobcode_id
        self.date = date
        self.hours = hours
        if locked:
            self.locked = locked


class PTO(db.Model):

    __tablename__ = 'pto'
    pto_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.user_id"), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    remaining = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.DateTime)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    from site import app, db
    print("connected to db")
