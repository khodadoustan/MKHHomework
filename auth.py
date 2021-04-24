from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

auth_app = Blueprint('auth', __name__,
                     template_folder='templates')


@auth_app.route('/login')
def login():
    return render_template('login.html')


@auth_app.route('/login', methods=['POST'])
def login_post():
    from models import User

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your username and password')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('shortlink.index'))


@auth_app.route('/signup')
def signup():
    return render_template('signup.html')


@auth_app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@auth_app.route('/signup', methods=['POST'])
def signup_post():
    from models import User
    from app import db

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:
        return redirect(url_for('auth.signup'))

    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
