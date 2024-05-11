import functools
from flask import Blueprint, render_template, request, url_for, redirect, session, g, flash
from media_record.db_manager import get_user, get_user_by_id
from media_record.db import db_session
from media_record.models import User
blp = Blueprint('auth', __name__)

@blp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id:
        g.user = get_user_by_id(user_id=user_id)
    else:
        g.user = None


@blp.get('/login')
def login_get():
    return render_template('login.html')

@blp.post('/login')
def login_post():
    username = request.form['username']
    password = request.form['password']

    user = get_user(username, password)

    if user:
        session.clear()
        session['user_id'] = user.user_id
        return redirect(url_for('records.index'))
    error = "BAD"
    flash(error)
    # return render_template('login.html')

@blp.post('/register')
def register_post():
    username = request.form['username']
    password = request.form['password']
    error = None
    if not username:
        error = 'Missing username'
    if not password:
        error = 'Missing password'
    
    if error is None:
        try:
            db_session.add(User(username, password))
            db_session.commit()
        except Exception as e:
            error = "Something is wrong: " + str(e)
        else:
            return redirect(url_for('auth.login_get'))
    
    flash(error)
    return render_template('register.html')

@blp.get('/register')
def register_get():
    return render_template('register.html')
@blp.get('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login_get'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login_get'))
        return view(**kwargs)
    return wrapped_view
    