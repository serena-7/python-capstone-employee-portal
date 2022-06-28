from site import db


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


class Jobcode(db.Model):

    __tablename__ = 'jobcodes'
    jobcode_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(200), nullable=False, unique=True)
    location = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


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


class PTO(db.Model):

    __tablename__ = 'pto'
    pto_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.user_id"), nullable=False)
    total_hours = db.Column(db.Integer, nullable=False)
    remaining_hours = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.Date)


if __name__ == "__main__":
    from site import app, db
    print("connected to db")
