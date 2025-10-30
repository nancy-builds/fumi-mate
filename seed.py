import json
import click
from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

@app.cli.command("seed-db")
def seed_db():
    """Seed the database from JSON file."""
    with app.app_context():

        User.query.delete()
        db.session.commit()

        # Seed DB
        user = User(
            username=u["username"],
            password_hash=generate_password_hash(u["password"])
        )
        db.session.add(user)
        db.session.commit()  # commit để có user.id

        db.session.commit()
        click.echo("Database seeded successfully!")
