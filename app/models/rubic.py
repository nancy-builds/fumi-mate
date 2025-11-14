from datetime import datetime
from ..extensions import db

class Rubric():
    __tablename__ = 'rubric'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    criteria = db.Column(db.Text) # JSON string with criteria and weights
    jlpt_level = db.Column(db.String(10), default='N5')