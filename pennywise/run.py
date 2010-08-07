#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main application entry point for testing. To run the test server::

  $ python setup.py develop
  $ python pennywise/run.py
"""

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_ECHO = True

if __name__ == '__main__':
    from pennywise import app
    app.config.from_object(__name__)
    from pennywise.models import db
    db.create_all()
    app.run()
