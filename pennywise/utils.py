# -*- coding: utf-8 -*-
"""
Utility functions. Some code adapted from http://github.com/mitsuhiko/flask/blob/website/flask_website/utils.py
"""

from functools import wraps
from flask import g, url_for, flash, request, redirect

def request_wants_json():
    """
    Return True if the request wants a JSON response.
    """
    # we only accept json if the quality of json is greater than the
    # quality of text/html because text/html is preferred to support
    # browsers that accept on */*
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

def requires_login(f):
    """
    Decorator to require a login for the given view.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('root.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function
