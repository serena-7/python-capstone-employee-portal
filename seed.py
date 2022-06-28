from company_site.models import User, Jobcode, Timecard, PTO
from datetime import datetime


def load_users():
    """Load users from users_data.txt in seed_data"""

    print("Loading Users Data")

    for row in open("seed_data/users_data.txt"):
        row = row.rstrip()
        user_id, email, password, first_name, last_name, phone_number, is_admin, is_active = row.split(
            "|")

        user = User(email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    is_admin=bool(is_admin),
                    is_active=bool(is_active)
                    )
        # add user to session
        db.session.add(user)
    # commit session
    db.session.commit()


def load_jobcodes():
    """Load jobcodes from jobcodes_data.txt in seed_data"""

    print("Loading Jobcodes Data")

    for row in open("seed_data/jobcodes_data.txt"):
        row = row.rstrip()
        jobcode_id, code, location, is_active = row.split("|")

        jobcode = Jobcode(code=code,
                          location=location,
                          is_active=bool(is_active)
                          )
        db.session.add(jobcode)

    db.session.commit()


def load_timecards():
    """Load timecards from timecards_data.txt in seed_data"""

    print("Loading Timecards Data")

    for row in open("seed_data/timecards_data.txt"):
        row = row.rstrip()
        user_id, jobcode_id, date, hours, is_locked = row.split("|")
        date = datetime.strptime(date, "%m/%d/%Y").date()

        timecard = Timecard(user_id=user_id,
                            jobcode_id=jobcode_id,
                            date=date,
                            hours=hours,
                            is_locked=bool(is_locked)
                            )
        db.session.add(timecard)

    db.session.commit()


def load_pto():
    """Load pto from pto_data.txt in seed_data"""

    print("Loading PTO Data")

    for row in open("seed_data/pto_data.txt"):
        row = row.rstrip()
        user_id, total, remaining, last_update = row.split("|")
        last_update = datetime.strptime(last_update, "%m/%d/%Y")

        pto = PTO(user_id=user_id,
                  total=total,
                  remaining=remaining,
                  last_update=last_update)
        db.session.add(pto)

    db.session.commit()


def reset_database():
    # Delete rows of tables in order of leaste dependencies
    PTO.query.delete()
    Timecard.query.delete()
    Jobcode.query.delete()
    User.query.delete()

    # reset sequences to 1
    db.session.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1; ALTER SEQUENCE jobcodes_jobcode_id_seq RESTART WITH 1; ALTER SEQUENCE timecards_timecard_id_seq RESTART WITH 1; ALTER SEQUENCE pto_pto_id_seq RESTART WITH 1;")

    print("Database Tables Reset")


if __name__ == "__main__":
    from company_site import db

    # create all tables in case they don't exists
    db.create_all()

    # reset the database
    reset_database()

    # load all data
    load_users()
    load_jobcodes()
    load_timecards()
    load_pto()
