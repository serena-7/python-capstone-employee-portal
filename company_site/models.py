from company_site import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(11), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, email, password, first_name, last_name, phone_number=None, is_admin=None, is_active=None):
        self.email = email
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        if phone_number:
            self.phone_number = phone_number
        if is_admin:
            self.is_admin = is_admin
        if is_active:
            self.is_active = is_active

    def check_password(self, given_password):
        return check_password_hash(self.password, given_password)


class Jobcode(db.Model):

    __tablename__ = 'jobcodes'
    jobcode_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(200), nullable=False, unique=True)
    location = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, code, location=None, is_active=None):
        self.code = code
        if location:
            self.location = location
        if is_active:
            self.is_active = is_active


class Timecard(db.Model):

    __tablename__ = 'timecards'
    timecard_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.user_id"), nullable=False)
    jobcode_id = db.Column(db.Integer, db.ForeignKey(
        "jobcodes.jobcode_id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Numeric(3, 2), nullable=False)
    is_locked = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, user_id, jobcode_id, date, hours, is_locked=None):
        self.user_id = user_id
        self.jobcode_id = jobcode_id
        self.date = date
        self.hours = hours
        if is_locked:
            self.is_locked = is_locked


class PTO(db.Model):

    __tablename__ = 'pto'
    pto_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.user_id"), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    remaining = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.DateTime)


if __name__ == "__main__":
    from site import app, db
    print("connected to db")
