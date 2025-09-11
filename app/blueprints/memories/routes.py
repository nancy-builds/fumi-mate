from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from . import bp

@bp.route("/memories")
def memories():
    return render_template("memories/memories.html", bg_url='images/bg.jpg')