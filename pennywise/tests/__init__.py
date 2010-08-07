"""
Unit tests for Pennywise.
"""

SQLALCHEMY_DATABASE_URI = 'sqlite://'
TESTING = True

def setup():
    from pennywise import app
    app.config.from_object(__name__)
