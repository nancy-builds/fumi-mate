from flask import render_template
from flask_login import login_required, current_user
from . import bp

@bp.route("/")
def home():
    return render_template("main/index.html")
