from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..models import Flashcard
from ..extensions import db

bp = Blueprint("api", __name__)

@bp.route("/flashcards")
@login_required
def get_flashcards():
    cards = Flashcard.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id": c.id, "front": c.front, "back": c.back} for c in cards])

@bp.route("/flashcards", methods=["POST"])
@login_required
def add_flashcard():
    data = request.json
    card = Flashcard(front=data["front"], back=data["back"], user_id=current_user.id)
    db.session.add(card)
    db.session.commit()
    return jsonify({"message": "Flashcard added"})
