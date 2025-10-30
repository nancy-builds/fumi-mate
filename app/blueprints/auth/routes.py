from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.extensions import db, login_manager
from app.models import User
from . import bp
from .forms import LoginForm, RegisterForm  # import form từ forms.py

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data

        # Database logic giữ nguyên
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('auth.register'))

        user = User(username=username,
                    password_hash=generate_password_hash(password),
                    role=role)

        db.session.add(user)
        db.session.commit()
        flash("Registered successfully. Please login.")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Look for the user in the database
        user = User.query.filter_by(username=username).first()

        # If user doesn't exist or password is incorrect
        if user is None or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password. Please try again.", "error")
            return redirect(url_for('auth.login'))

        # If login successful
        login_user(user)
        flash("Login successful!", "success")
        return redirect(url_for('main.home'))

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
