#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main application entry point for testing. To run the test server::

  $ python setup.py develop
  $ python pennywise/run.py
"""

from pennywise import app
import pennywise.views

def initdb():
    from pennywise.models import db
    db.create_all()


# These settings come into effect only if the call to app.config.from_object(__name__)
# below goes through. It's safe to import this module without side-effects.
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_ECHO = False

if __name__ == '__main__':
    app.config.from_object(__name__)
    initdb()
    app.run('0.0.0.0', 8080, debug=False)
