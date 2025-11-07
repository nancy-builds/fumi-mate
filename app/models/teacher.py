from ..extensions import db
from .user import User

class Teacher(User):
    __tablename__ = "Teacher"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bio = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }