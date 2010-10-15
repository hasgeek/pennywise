# -*- coding: utf-8 -*-

from flask import request, abort, render_template, url_for
from pennywise import app
from pennywise.models import User
from pennywise.ledgers import get_ledgers


@app.route('/<username>/')
def userpage(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    showhidden = True if request.args.get('showhidden') else False # Sanitize untrusted data
    print "Showhidden", showhidden
    ledgers = get_ledgers(user.ledger)
    return render_template('ledgers.html', user=user, ledgers=ledgers[1:], multicurrency=False, maincurrency='INR')
