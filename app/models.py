from app.extensions import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    sets = db.relationship("FlashcardSet", backref="owner", lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class FlashcardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    flashcards = db.relationship("Flashcard", backref="flashcard_set", lazy=True)

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(200), nullable=False)
    back = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10))  # forget / know / forget
    set_id = db.Column(db.Integer, db.ForeignKey("flashcard_set.id"), nullable=False)