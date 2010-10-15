# -*- coding: utf-8 -*-

"""
Operations on ledgers.
"""

from flask import url_for
from pennywise.models import db, Ledger, LEDGER_TYPE, LEDGER_SUBTYPE


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
    return result


def make_default_ledgers(userledger):
    """
    Make some default ledgers to help the user get started
    """
    commodity = userledger.commodity

    assets = Ledger(parent=userledger, title=u'Assets', description=u'All current assets', placeholder=True, ltype=LEDGER_TYPE.ASSET, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)
    liabilities = Ledger(parent=userledger, title=u'Liabilities', description=u'All current liabilities', placeholder=True, ltype=LEDGER_TYPE.LIABILITY, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)
    income = Ledger(parent=userledger, title=u'Income', description=u'All sources of income', placeholder=True, ltype=LEDGER_TYPE.INCOME, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)
    expenses = Ledger(parent=userledger, title=u'Expenses', description=u'All expenses', placeholder=True, ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)
    equity = Ledger(parent=userledger, title=u'Equity', description=u'Financial infusions', placeholder=True, ltype=LEDGER_TYPE.EQUITY, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)

    db.session.add(assets)
    db.session.add(liabilities)
    db.session.add(income)
    db.session.add(expenses)
    db.session.add(equity)

    cash = Ledger(parent=assets, title=u'Cash', description=u'Cash in my wallet', ltype=LEDGER_TYPE.ASSET, lsubtype=LEDGER_SUBTYPE.CASH, commodity=commodity)
    bank = Ledger(parent=assets, title=u'Bank', description=u'My bank account', ltype=LEDGER_TYPE.ASSET, lsubtype=LEDGER_SUBTYPE.BANK, commodity=commodity)

    db.session.add(cash)
    db.session.add(bank)

    creditcard = Ledger(parent=liabilities, title=u'Credit Card', description=u'My credit cards', ltype=LEDGER_TYPE.LIABILITY, lsubtype=LEDGER_SUBTYPE.CREDITCARD, commodity=commodity)

    db.session.add(creditcard)

    salary = Ledger(parent=income, title=u'Salary', description=u'Income from current and previous employers', ltype=LEDGER_TYPE.INCOME, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)
    hobbies = Ledger(parent=income, title=u'Hobbies', description=u'Income from hobbies', ltype=LEDGER_TYPE.INCOME, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)
    gifts = Ledger(parent=income, title=u'Gifts', description=u'Cash gifts', ltype=LEDGER_TYPE.INCOME, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)

    db.session.add(salary)
    db.session.add(hobbies)
    db.session.add(gifts)

    rent = Ledger(parent=expenses, title=u'Rent', description=u'Monthly house rent', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)
    emi = Ledger(parent=expenses, title=u'EMI', description=u'Monthly payments for the house and car', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)
    food = Ledger(parent=expenses, title=u'Food', description=u'Breakfast, lunch and dinner', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)
    shopping = Ledger(parent=expenses, title=u'Shopping', description=u'All purchases', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity)

    db.session.add(rent)
    db.session.add(emi)
    db.session.add(food)
    db.session.add(shopping)

    opening = Ledger(parent=equity, title=u'Opening Balances', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, commodity=commodity, hidden=True)

    db.session.add(opening)
