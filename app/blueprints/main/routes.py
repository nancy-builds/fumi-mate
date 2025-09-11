from flask import render_template
from flask_login import login_required, current_user
from . import bp   # import blueprint "main" từ __init__.py

@bp.route("/")
def home():
    return render_template("main/index.html", bg_url='images/bg.jpg')
