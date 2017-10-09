import string
from .. import db
class Task(db.Model):
    """
    Database model for an `Event`'s `Task`s
    """
    
    id = db.Column(db.Integer, primary_key=True)
    """
    The primary key
    
    **Type:** INTEGER PRIMARY KEY
    """
    
    part_id = db.Column(db.Integer, db.ForeignKey("participant.id"))
    """
    The id of the `Participant` that this `Task` belongs to
    
    **Type:** INTEGER FOREIGN KEY
    """

    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    """
    The id of the `Event` that this `Task` belongs to
    
    **Type:** INTEGER FOREIGN KEY
    """

    task = db.Column(db.Text)
    """
    The name of the `Task`
    
    **Type:** TEXT
    """
    
    is_assigned = db.Column(db.Boolean)
    """
    Whether the `Task` has been assigned to participant or not
    
    **Type:** BOOLEAN
    """
    
    participant = db.relationship("Participant")
    """
    Relationship to the `Participant` that this `Task` belongs to
    
    **Related Model:** `event_planner.models.Participant`
    """

    event = db.relationship("Event")
    """
    Relationship to the `Event` that this `Task` belongs to
    
    **Related Model:** `event_planner.models.Event`
    """
    
    def __init__(self, task, is_assigned, part_id, event_id):
        """Creates a new `Task` instance"""

        self.task = task
        self.is_assigned = is_assigned
        self.part_id = part_id
        self.event_id = event_id