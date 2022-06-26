# Data Model Brainstorm

### Users Table

- user ID
- email
- password
- first name
- last name
- phone number
- privledges

### Timecards Table

- timecard ID
- date
- hours
- jobcode ID
- user ID
- locked

### Jobcodes Table

- jobcode id
- jobcode name
- location
- active

### PTO Table

- PTO id
- user ID
- total hours
- hours remaining
- date last updated
