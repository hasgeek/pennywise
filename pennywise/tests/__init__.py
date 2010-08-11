"""
Unit tests for Pennywise.
"""

SQLALCHEMY_DATABASE_URI = 'sqlite://'
TESTING = True
CSRF_ENABLED = False


def setup():
    from pennywise import app
    app.config.from_object(__name__)
