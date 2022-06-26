CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  user_email VARCHAR(100) NOT NULL UNIQUE,
  user_password VARCHAR(500) NOT NULL,
  first_name VARCHAR(25) NOT NULL,
  last_name VARCHAR(25) NOT NULL,
  phone_number VARCHAR(11),
  admin_privledge BOOLEAN DEFAULT 'f',
  active BOOLEAN DEFAULT 't'
);

CREATE TABLE jobcodes (
  jobcode_id SERIAL PRIMARY KEY,
  jobcode VARCHAR(100) NOT NULL,
  location VARCHAR(500),
  active BOOLEAN DEFAULT 't'
);

CREATE TABLE timecards (
  timecard_id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(user_id),
  jobcode_id INT NOT NULL REFERENCES jobcodes(jobcode_id),
  timecard_date DATE NOT NULL,
  hours NUMERIC NOT NULL,
  locked BOOLEAN DEFAULT 'f'
);

CREATE TABLE pto (
  pto_id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(user_id),
  total_hours INT NOT NULL,
  remaining_hours INT NOT NULL,
  last_update DATE
);