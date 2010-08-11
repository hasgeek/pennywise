# -*- coding: utf-8 -*-

from flask import request, abort, render_template, url_for
from pennywise import app
from pennywise.models import User


def get_ledgers(baseledger):
    """
    Return ledgers as an array of {level, ledger} dictionaries. Uses recursion.
    """
    def loop(base, level):
        if base.title == 'Equity':
            debug = True
        else:
            debug = False
        hidden = base.hidden
        if debug: print "hidden", base, base.hidden
        result = [{'level': level, 'url': url_for('ledger', uuid=base.uuid), 'hidden': hidden, 'ledger': base}]
        allsubhidden = True
        for ledger in base.subledgers:
            subledgers, subhidden = loop(ledger, level+1)
            result.extend(subledgers)
            # If current ledger is hidden, hide all subledgers (unless they are already hidden)
            if hidden and not subhidden:
                for r in result[1:]:
                    r['hidden'] = True
                subhidden = True
            if not subhidden:
                allsubhidden = False
        # If this is a placeholder and everything below is hidden, hide this too
        if base.placeholder and allsubhidden:
            hidden = True
            result[0]['hidden'] = True
        return result, hidden
    result, hidden = loop(baseledger, 0)
    return result[1:] # Remove baseledger itself


@app.route('/<username>/')
def userpage(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    showhidden = True if request.args.get('showhidden') else False # Sanitize untrusted data
    print "Showhidden", showhidden
    ledgers = get_ledgers(user.ledger)
    return render_template('ledgers.html', user=user, ledgers=ledgers, multicurrency=False, maincurrency='INR')
