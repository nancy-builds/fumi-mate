from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()


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


@app.route("/")
def home():
    return render_template("index.html", bg_url='images/bg.jpg')

@app.route('/flashcards')
def flashcards():
    return render_template("flashcards/flashcards.html", topics_data=topics)

@app.route('/flashcards/<topic>')
def deck(topic):
    return render_template("flashcards/deck.html",
                               data=topics[topic])









@app.route('/memories')
def memories():
    return render_template("memories.html")

@app.route('/games')
def games():
    return render_template("games.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run()

