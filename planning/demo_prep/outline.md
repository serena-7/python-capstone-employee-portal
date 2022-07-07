# DEMO PREP OUTLINE

## Personal Bio

- I'm Serena Sorensen
- I have a background in chemical engineering and have navigated into, what I believe to be my calling, software engineering.

## Project Bio

- This is my capstone project at Devmountain.
- I chose to create an employee portal for my dad's small business.
- They currently do time tracking on a google sheet but my dad wanted an application and database for his employees to use.
- I structured the entrie application to be scalable with blueprints to allow for additional features as I build my dad's company website.

## Features

#### Software Stack:

- This is a Flask Application in Python
- Using a PostgreSQL Database
- Boostrap for styling
- and is Currently hosted on Heroku

#### Main Page:

- This is the Basic Homepage for the entire company site
- I built out the employee portal portion
- Link to employee portal

#### Login:

- All session management for logging in and out was done using flask-login's LoginManager

### Employee without Admin Privledges:

- Dashboard Welcomes Employees to the Portal

#### Timecards:

- The launch page for timecards shows the current week.
- Previous and Next buttons navigate to other weeks which are calculated using python datetime functions.
- This table is a form and each row within the table is a sub form. WTForms allows this kind of generation using the FieldList feature.
- To fill in your time entries for the week:
  - Select Jobcode from the drop down list which retrieves all active jobcodes in the database.
  - Enter time spent on that jobcode in the same row on each day.
  - Multiple jobcodes can be used in one week and any empty rows will be ignored when submitted.
  - Click Submit Time Entries to save all data in the database.
- How it submits:
  - The server iterates over the sub forms in the main form. If a jobcode is selected for that row it iterates through the weekdays and saves each cell as it's own entry into the database using flask-sqlalchemy methods.
  - if the input field is blank it doesn't save anything.
- Clear and Delete:
  - Clear unsaved will clear any entries that were not already saved to the database but will not delete time entries in the database.
  - If you need to delete a time entry change the value to 0 and click submit. This will delete the entry entirely.
- To view past weeks simply use navigation buttons
- if the timecards are locked for that week the submit button will not be displayed and no changes can be made.

#### Account:

- The account page shows you your user information and allows you to edit certain info with the blue buttons.

#### Logout:

- clicking logout will simply log you out.

### Employee with Admin Privledges:

- Another row of tabs is visible if the employee has admin privledges.

#### Manage Employees:

- Shows a list of all employees split into categories.
- View Info allows you to see and then edit employee information
- The options drop down gives the options available for that employee.
- If you select change password it will take you to a form to change that employees password.
- If you select another option a pop up will ask if you are sure. If you click yes it will update the info in the database and reload the list.
- Add New Employee works like a registration page only admins can create new users.

#### Manage Jobcodes:

- Shows a list of all jobcodes split into active and inactive categories.
- You can edit the jobcode name and location using an edit button
- The other option allows you to deactivate or reactivate a jobcode.
- Only active jobcodes will show up in the drop down for employees to select in their timecards.
- Add new jobcode allows you to create a new jobcode.

## Thoughtful Ending

#### What I learned:

- How to iterate through forms and subforms and dates to make table cells that represent entries into the database

#### Future Plans:

- Manage Timecards will allow an admin to view each employees timecards.
- Create reports for payroll
- Keep track of PTO
- I plann to host the production website and database on AWS
- to have a full functioning company website for my dad's business
