from ..extensions import db
from .user import User

class Student(User):
    __tablename__ = "student"

    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    grade = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }