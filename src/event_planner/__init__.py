from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from . import defaults
#Define the global flask app
app = Flask(__name__)
app.config.from_object(defaults)
#Insert stuff into the templating engine's world
from . import utils
app.jinja_env.globals.update(all_timeslots=utils.all_timeslots(),
    enumerate=enumerate)
#Start SQLAlchemy
db = SQLAlchemy(app)
#The imports come later so that the app and db objects are in existence
from . import models
from . import views
#TODO: move migrations out
db.create_all()
#Static files here
# url_for('static', filename='style.css')
# url_for('static', filename='script.js')
# url_for('static', filename='toolkit-inverse.min.css')
# url_for('static', filename='toolkit.min.js')
