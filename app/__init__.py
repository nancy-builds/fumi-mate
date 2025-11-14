from flask import Flask
import os
from app.extensions import db, migrate, login_manager
from .blueprints.main import bp as main_bp
from .blueprints.auth import bp as auth_bp
from .blueprints.teacher import bp as teacher_bp
from .blueprints.student import bp as student_bp
from app.models import User, Teacher, Student
from dotenv import load_dotenv
from app.core.rag_pipeline import RAGPipeline
from app.core.langchain_agents import FeedbackAgents

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        db.create_all()

    pipeline = RAGPipeline(persist_directory="./submissions_db")
    agents = FeedbackAgents()

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(teacher_bp, url_prefix="/teacher")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(main_bp)

    # ép môi trường development
    os.environ["FLASK_ENV"] = "development"
    app.debug = True

    return app


