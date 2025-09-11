from flask import Blueprint

bp = Blueprint("memories", __name__, template_folder="templates")

from . import routes