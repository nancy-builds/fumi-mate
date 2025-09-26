from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from . import bp
@bp.route("/")
@login_required
def index():
    return render_template("profile/index.html", bg_url='images/bg.jpg')
