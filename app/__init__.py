from flask import Flask
import os
from app.extensions import db, migrate, login_manager
from .blueprints.main import bp as main_bp
from .blueprints.auth import bp as auth_bp
from .blueprints.flashcards import bp as flashcards_bp
from .blueprints.memories import bp as memories_bp
from .blueprints.profile import bp as profile_bp
from .models import User

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(flashcards_bp, url_prefix="/flashcards")
    app.register_blueprint(memories_bp, url_prefix="/memories")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(main_bp)

    # ép môi trường development
    os.environ["FLASK_ENV"] = "development"
    app.debug = True

    return app