# -*- coding: utf-8 -*-

from pennywise.app import app

@app.route('/<username>/')
def userpage(username):
    return "User: %s" % username
