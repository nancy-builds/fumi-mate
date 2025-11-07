from ..extensions import db
from .user import User

class Student(User):
    __tablename__ = "Student"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    grade = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }