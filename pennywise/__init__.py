"""
Pennywise is a web-based multi-user double-entry accounting application using the Flask framework.
"""
from flask import Flask
app = Flask(__name__)
app.config.from_object('pennywise.default_settings')

__version__ = '0.1'
