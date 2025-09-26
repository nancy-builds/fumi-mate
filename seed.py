import json
import click
from app import create_app
from app.extensions import db
from app.models import User, FlashcardSet, Flashcard
from werkzeug.security import generate_password_hash

app = create_app()

@app.cli.command("seed-db")
def seed_db():
    """Seed the database from JSON file."""
    with app.app_context():

        # Clear old data
        Flashcard.query.delete()
        FlashcardSet.query.delete()
        db.session.commit()

        # Load JSON
        with open("data/flashcards.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        # Clear DB
        Flashcard.query.delete()
        FlashcardSet.query.delete()
        User.query.delete()
        db.session.commit()

        # Seed DB
        for u in data["users"]:
            user = User(
                username=u["username"],
                password_hash=generate_password_hash(u["password"])
            )
            db.session.add(user)
            db.session.commit()  # commit để có user.id

            for s in u.get("sets", []):
                flashcard_set = FlashcardSet(
                    name=s["name"],
                    user_id=user.id
                )
                db.session.add(flashcard_set)
                db.session.commit()  # commit để có set.id

                for card in s.get("flashcards", []):
                    flashcard = Flashcard(
                        front=card["front"],   # updated
                        back=card["back"],     # updated
                        status=card.get("status", "new"),
                        set_id=flashcard_set.id
                    )
                    db.session.add(flashcard)

        db.session.commit()
        click.echo("Database seeded successfully!")
