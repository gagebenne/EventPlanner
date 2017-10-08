import datetime
from wtforms import Form, SelectField, SubmitField, StringField, BooleanField, DateField, Field, FieldList, FormField, SelectMultipleField, validators
from wtforms.validators import DataRequired, Optional, ValidationError
from wtforms.widgets import HiddenInput
from .. import utils

class TimeslotInput(HiddenInput):
    """
    Widget for rendering a timeslot button
    """
    def __init__(self, timeslot):
        self._timeslot = timeslot
        super(TimeslotInput, self).__init__()

    def __call__(self, field, **kwargs):
        class_ = kwargs.pop("class_", "")
        val = field.data[0] if hasattr(field.data, "__len__") else field.default

        html = ["<div id=\"slot_button_%s\" class=\"timeslot\">" % field._timeslot.strftime("%H%M")]
        html.append("<p class=\"12-hour-form\">%s</p>" % self._timeslot.strftime("%I:%M %p"))
        html.append("<p class=\"24-hour-form\">%s</p>" % self._timeslot.strftime("%H:%M"))
        html.append("<input type=\"hidden\" class=\"%s\" value=\"%s\" name=\"%s\"/>" % (class_, ("1" if val else "0"), field.name))
        html.append("</div>")

        if val is True:
            #jQuery UI selectable workaround
            html.append("<script> $(document).ready(function() {$(\"#slot_button_%s\").removeClass(\"ui-selected\").addClass(\"ui-selected\").addClass(\"active\");});</script>" % self._timeslot.strftime("%H%M"))

        return "\n".join(html)

class TimeslotField(BooleanField):
    def __init__(self, label="", validators=None, timeslot=datetime.time(), **kwargs):
        super(TimeslotField, self).__init__(label, validators, default=False, **kwargs)
        self.widget = TimeslotInput(timeslot)
        self._timeslot = timeslot
    def process_formdata(self, value_list):
        self.data = [i == "1" for i in value_list]
    @property
    def timeslot(self):
        return self._timeslot

def with_timeslots(form_type, timeslots):
    """Returns `EventForm` as if it were declared with the given timeslots"""
    #TODO: Consider using interning since this is probably crazy slow
    ugly_type_suffix = "_".join([t.strftime("%H%M") for t in timeslots])

    #When copy.deepcopy() just won't do, simulate inheiritance and learn to love duck typing
    #This is needed because the copy module can't handle types...
    fresh_type = type(form_type.__name__+"With"+ugly_type_suffix, form_type.__bases__, dict(form_type.__dict__))

    for timeslot in timeslots:
        field_name = "slot_" + timeslot.strftime("%H%M")
        setattr(fresh_type, field_name, TimeslotField(field_name, [Optional()], timeslot=timeslot))
    fresh_type.timeslots = timeslots

    return fresh_type

class TaskForm(Form):
    """
    `Form` used for creating new `Task`s
    """
    name = StringField("taskname", [DataRequired(message='Task cannot be empty'), validators.Length(max=20, message='Task name cannot exceed 20 characters')])

def validate_timeslots(form, field):
    displayError = True
    for timeslot in form.timeslots:
        val = form["slot_%s" % timeslot.strftime("%H%M")].data[0]
        if val is True:
            displayError = False
            break
    if displayError:
        raise ValidationError('Must select at least one timeslot')

def validate_date(form, field):
    if not isinstance(form.date.data, datetime.date):
        #An error is already being printed from somewhere else,
        # since WTForm automatically displays an error for improper format
            x = 1+1 #placeholder
        #raise ValidationError('Invalid date format, use MM/DD/YYYY')
    elif (form.date.data < datetime.date.today()):
        raise ValidationError('Cannot choose a date in the past')

class EventForm(Form):
    """
    `Form` used for creating new `Event`s
    """
    eventname = StringField("eventname", [DataRequired(message='Event Name cannot be empty'), validators.Length(max=25, message='Event Name cannot exceed 25 characters')])
    eventdescription = StringField("eventdescription", [validators.Length(max=50, message='Description cannot exceed 50 characters')])  # Calls timeslot validation
    adminname = StringField("adminname", [DataRequired(message='Admin Name cannot be empty')])
    date = DateField("date", [validate_date, validate_timeslots], format="%m/%d/%Y")

    @staticmethod
    def default_form(timeslots=utils.all_timeslots()):
        return with_timeslots(EventForm, timeslots)

class ParticipantTaskForm(Form):
    participantname = StringField("participantname", [DataRequired(message='Participant Name cannot be empty')])
    participanttasks = SelectField(
        'Tasks',
        choices=[],
        coerce=int
    )
    submit = SubmitField("Submit")

class ParticipantForm(Form):
    """
    `Form` used for creating new `Participant`s
    """
    participantname = StringField("participantname")
    date = DateField("date", [validate_date], format="%m/%d/%Y")

    def validate_participantname(form, field):
        """
        Does validation for participants, ie signing up for an event.
        Note: This never dispays errors, since on hitting submit the page redirects.
        However, the errors are raised, and it is prevented from being added.
        Since timeslots is weird, we also do valiation for it here.
        :param field: Params will be passed in automatically based on how validation is defined.
        :return: If invalid, a validation error.
        """
        if field.data == '':
            raise ValidationError('Participant Name cannot be empty')

        # Also does validation for timeslots here, since there's no other place for it.
        """ CURRENTLY DEPRECATED
        displayError = True
        for timeslot in form.timeslots:
            val = form["slot_%s" % timeslot.strftime("%H%M")].data[0]
            if val is True:
                displayError = False
                break
        if displayError:
            raise ValidationError('Must select at least one timeslot')
        """

    @staticmethod
    def default_form(timeslots=utils.all_timeslots()):
        return with_timeslots(ParticipantForm, timeslots)

class DateForm(Form):
    """
    `Form` used for creating new `Date`s
    """
    date = DateField("date", [validate_date], format="%m/%d/%Y")

    @staticmethod
    def default_form(timeslots=utils.all_timeslots()):
        return with_timeslots(DateForm, timeslots)
