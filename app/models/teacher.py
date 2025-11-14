from ..extensions import db
from .user import User

class Teacher(User):
    __tablename__ = "Teacher"

    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    bio = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }