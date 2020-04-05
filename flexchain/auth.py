from functools import wraps

from flask import session, request, redirect, url_for

from .models.user import login_user


def get_auth_storage():
    if 'auth' not in session:
        session['auth'] = dict()
    return session['auth']


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(request.remote_addr, get_auth_storage())
        if request.remote_addr not in get_auth_storage():
            print('Not recognized')
            return redirect(url_for('login'))
        print('Successfully logged in')
        return f(*args, **kwargs)
    return decorated_function


def perform_login(cursor, email, password):
    authorizations = get_auth_storage()
    first_name = login_user(cursor, email, password)
    if first_name:
        authorizations[request.remote_addr] = first_name
        session['auth'] = authorizations
        print(session['auth'])
        return True
    print(authorizations)
    print(first_name)
    return False
