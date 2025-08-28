from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..forms.forms import FlashcardForm
from ..models import Flashcard
from ..extensions import db

bp = Blueprint("main", __name__)

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

@bp.route("/")
def home():
    return render_template("index.html", bg_url='images/bg.jpg')

@bp.route("/memories")
def memories():
    return render_template("memories.html", bg_url='images/bg.jpg')

@bp.route("/games")
def games():
    return render_template("games.html", bg_url='images/bg.jpg')

@bp.route("/profile")
def profile():
    return render_template("profile.html", bg_url='images/bg.jpg')

