# -*- coding: utf-8 -*-

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
    return '' # FIXME: Redirect to static resource
