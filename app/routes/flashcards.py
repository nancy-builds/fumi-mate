from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..forms.forms import FlashcardForm
from ..models import Flashcard
from ..extensions import db
from flask_login import login_required, current_user


bp = Blueprint("auth", __name__, url_prefix="/auth")

topics = {
    "japan": {
        "title": "Japanese 🇯🇵",
        "description": "Learn Japanese vocabulary and Kanji with interactive tools designed for efficient study.",
        "flashcards": [
            {"front": "こんにちは", "back": "Hello"},
            {"front": "ありがとう", "back": "Thank you"},
            {"front": "さようなら", "back": "Goodbye"},
        ]
    },
    "vietnam": {
        "title": "Vietnamese 🇻🇳",
        "description": "Learn Japanese vocabulary and Kanji with interactive tools designed for efficient study.",
        "flashcards": [
            {"front": "Xin chào", "back": "Hello"},
            {"front": "Cảm ơn", "back": "Thank you"},
            {"front": "Tạm biệt", "back": "Goodbye"},
        ]
    },
    "vit": {
        "title": "Vietnamese 🇻🇳",
        "description": "Learn Japanese vocabulary and Kanji with interactive tools designed for efficient study.",
        "flashcards": [
            {"front": "Xin chào", "back": "Hello"},
            {"front": "Cảm ơn", "back": "Thank you"},
            {"front": "Tạm biệt", "back": "Goodbye"},
        ]
    },
    "nam": {
        "title": "Vietnamese 🇻🇳",
        "description": "Learn Japanese vocabulary and Kanji with interactive tools designed for efficient study.",
        "flashcards": [
            {"front": "Xin chào", "back": "Hello"},
            {"front": "Cảm ơn", "back": "Thank you"},
            {"front": "Tạm biệt", "back": "Goodbye"},
        ]
    }
}

@bp.route('/flashcards')
@login_required
def flashcards():
    return render_template("flashcards/flashcards.html", topics_data=topics)

@bp.route('/flashcards/<topic>')
@login_required
def deck(topic):
    return render_template("flashcards/deck.html",
                               data=topics[topic])




@bp.route("/")
@login_required
def index():
    if current_user.is_authenticated:
        flashcards = Flashcard.query.filter_by(user_id=current_user.id).all()
    else:
        flashcards = []
    return render_template("index.html", flashcards=flashcards)

@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_flashcard():
    form = FlashcardForm()
    if form.validate_on_submit():
        card = Flashcard(front=form.front.data, back=form.back.data, user_id=current_user.id)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("add.html", form=form)

