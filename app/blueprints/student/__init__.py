from flask import Blueprint
from app.core.rag_pipeline import RAGPipeline
from app.core.langchain_agents import FeedbackAgents

bp = Blueprint("student", __name__, template_folder="templates", static_folder="static")
pipeline = RAGPipeline(persist_directory="./submissions_db")
agents = FeedbackAgents()

from . import routes
