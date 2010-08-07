# -*- coding: utf-8 -*-

from flask import redirect, url_for
from pennywise.app import app

@app.route('/')
def index():
    return "Root!"

@app.route('/logout/')
def logout():
    pass

@app.route('/favicon.ico')
@app.route('/favicon.ico/')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'), code=301)
