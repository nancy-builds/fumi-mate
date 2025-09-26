from flask import Blueprint

bp = Blueprint("pomodoro", __name__, template_folder="templates", static_folder="static")

from . import routes