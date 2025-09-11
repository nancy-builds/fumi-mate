from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import FlashcardSet, Flashcard
from . import bp

@bp.route('/')
@login_required
def index():
    sets = FlashcardSet.query.filter_by(user_id=current_user.id).all()
    return render_template('flashcards/index.html', sets=sets)

@bp.route('/<set_name>')
@login_required
def flashcards(set_name):
    flashcard_set = FlashcardSet.query.filter_by(
        name=set_name, user_id=current_user.id
    ).first_or_404()
    cards = Flashcard.query.filter_by(set_id=flashcard_set.id).all()
    return render_template('flashcards/flashcards.html', flashcard_set=flashcard_set, cards=cards)

@bp.route('/update_status', methods=['POST'])
@login_required
def update_status():
    data = request.get_json()
    card_id = data['card_id']
    status = data['status']

    card = Flashcard.query.get_or_404(card_id)
    parent_set = FlashcardSet.query.get(card.set_id)

    if parent_set.user_id != current_user.id:
        return jsonify(success=False, error="Unauthorized"), 403

    card.status = status
    db.session.commit()
    return jsonify(success=True)

@bp.route('/retry/<set_name>')
@login_required
def retry(set_name):
    flashcard_set = FlashcardSet.query.filter_by(
        name=set_name, user_id=current_user.id
    ).first_or_404()
    cards = Flashcard.query.filter_by(set_id=flashcard_set.id, status="forget").all()
    return render_template('flashcards.html', flashcard_set=flashcard_set, cards=cards)
