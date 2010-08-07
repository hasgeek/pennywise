# -*- coding: utf-8 -*-

from pennywise.app import app

@app.route('/ledger/<uuid>/')
def ledger(uuid):
    return "Ledger: %s" % uuid
