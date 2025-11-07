from flask import Blueprint

bp = Blueprint("student", __name__, template_folder="templates", static_folder="static")

from . import routes
