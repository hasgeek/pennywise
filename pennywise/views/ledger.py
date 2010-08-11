# -*- coding: utf-8 -*-

from flask import abort, render_template
from pennywise import app
from pennywise.models import Ledger

@app.route('/ledger/<uuid>/')
def ledger(uuid):
    ledger = Ledger.query.filter_by(uuid=uuid).first()
    if ledger is None:
        abort(404)
    rootledger = ledger
    while rootledger.parent is not None:
        rootledger = rootledger.parent
    owner = rootledger.owner
    return render_template('transactions.html', owner=owner, ledger=ledger)
