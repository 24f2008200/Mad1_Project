# Note of Caution

## I am trying to document the process of developing this app.
### this lines are to test the skills in using markup, as I learn.


<picture>
 <source media="(prefers-color-scheme: dark)" srcset="YOUR-DARKMODE-IMAGE">
 <source media="(prefers-color-scheme: light)" srcset="YOUR-LIGHTMODE-IMAGE">
 <img alt="YOUR-ALT-TEXT" src="YOUR-DEFAULT-IMAGE">
</picture>



~~This was mistaken text~~

Hi, I'm Baskaran. You might recognize me as GitHub's newbie.

| Rank | Languages |
|-----:|-----------|
|     1| JavaScript|
|     2| Python    |
|     3| SQL       |


# About the System
## About the _macro.html
The _macro.html is the key renderer and it renders:
1. tabs -> creates tabs and depending upon what is inside the tab renders those sub components.
2. renders normal table with action buttons, if required
3. render filter  tables with jscript for filter
4. render form
5. render blank page

# About routes

| End Point       | Module |  Function                 |
|----------------:|--------|---------------------------|
| /login          | app.py |  Check pwd set the role and user in current user|
| /logout       | app.py |  Function                 |
| /register       | patient.py |  Collects & check email is free & register  |
| /patient/dashboard| patient.py |  Compiles dashboard info |
| /patient/appointments_book | patient.py |  Checks availability & books -uses /doctor/availability |
| /patient/delete_appointment| patient.py |  Delets the appointment & raise alert |
| /patient/history| patient.py |  compiles the treatment history and displays |
| /patient/edit_appointment| patient.py |  Just shows the details of appointment- not allowed to modify. |
| /doctor/edit| doctor.py |  edits doctor profile |
| /doctor/dashboard| doctor.py |  Compiles dashboard info |
| /doctor/mark_availability| doctor.py |  Displays calendar for doctor |
| /doctor/update_appointment| doctor.py |  Updates the appointment, Treatment |
| /doctor/edit_availability| doctor.py |  Edits availability if free|
| /doctor/doctor_availability| doctor.py |  Displays calendar for patient |
| /doctor/close_appointment| doctor.py |  Close the appointment - no more modification |
| /doctor/cancel_appointment| doctor.py |  Delets the appointment & raise alert |

| /doctor/edit| doctor.py |  edits doctor profile |
| /doctor/edit| doctor.py |  edits doctor profile |
| /doctor/edit| doctor.py |  edits doctor profile |
| /doctor/edit| doctor.py |  edits doctor profile |
