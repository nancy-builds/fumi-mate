from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from . import bp
@bp.route("/profile")
@login_required
def profile():
    return render_template("profile/profile.html", bg_url='images/bg.jpg')
