********************************************************************************************
EECS 448 Project 1 (Fall 2017)
********************************************************************************************

Design
====================

MVC Pattern
^^^^^^^^^^^^^
* Database Models
    * events
        * Fields
            * title: *string*
            * description: *string*
            * id: *integer, primary key*
            * admin_link: *string*
        * Relations
            * participants: *one-to-many*
    * participant
        * Fields
            * name: *string*
            * id: *integer, primary key*
            * is_admin: *boolean*
        * Relations
            * timeslots: *one-to-many*
            * tasks: *one-to-many*
    * timeslot
        * Fields
            * part_id: *integer, foreign key*
            * timeslot: *datetime*
    * tasks
        *Fields
            * part_id: *integer, foreign key*
            * task: *string*
* Views
* Controllers

Account-less authentication scheme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. An anonymous user creates an event
#. A session is created that owns this event
#. A 'magic link' is presented to the user to create a new session if they lose their current one. This can also be used to share ownership of an event.

Stretch Goals
=============

1. Implement the above authenication scheme
#. Add an option to email the 'magic link' upon event creation so that the user has easy access to it after they close the app.
#. Add an option to email a link to the event upon a non-owner adding their availability


Setting up Locally
====================
* Requirements: Everything in the Implementation section below

1. In Postgres, execute the following commands: 

``create role evplanner with password 'evplanner'``

``\connect evplanner``

``create database evplanner``

2a. On Windows, ensure you're at the top level of this project in command prompt and execute the following command:

``set FLASK_APP=src/event_planner/__init__.py``

2b. On OSX/Unix, ensure you're at the top level of this project in terminal and execute the following command:

``export FLASK_APP="src/event_planner/__init__.py"``

3. In command prompt or terminal, run the following commands:

``flask migrate``

``flask run``

4. The app should now be live on some port on localhost. Your terminal will tell you which.


Implementation
==============
* Python 3
* Flask (Views and Controllers)
* SQLAlchemy (Models)
* Postgresql (Database)
* Jinja2 (Templates)
* JQuery & JQuery UI (DOM Manipulation)
* Bootstrap 4 (CSS Framework)
* DateUtil

Expansion
==============
* On this fork, we have implemented the following features, in addition to everything on the original repo:
* It is now possible to create events with multiple dates.
* When adding a new day, it is possible to create multiple in a row with the same timeslots.
* Tasks are now implemented. Admins can create tasks for their events and participants can sign up for unassigned tasks.
* Claiming these tasks is a unique action; only one person can claim each event.
* All of the above is designed to be intuitive in the UI.

