# -*- coding: utf-8 -*-

"""
Operations on ledgers.
"""

from pennywise.models import db, Ledger, LEDGER_TYPE, LEDGER_SUBTYPE


def make_default_ledgers(userledger):
    """
    Make some default ledgers to help the user get started
    """
    currency = userledger.currency

    assets = Ledger(parent=userledger, title=u'Assets', description=u'All current assets', placeholder=True, ltype=LEDGER_TYPE.ASSET, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)
    liabilities = Ledger(parent=userledger, title=u'Liabilities', description=u'All current liabilities', placeholder=True, ltype=LEDGER_TYPE.LIABILITY, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)
    income = Ledger(parent=userledger, title=u'Income', description=u'All sources of income', placeholder=True, ltype=LEDGER_TYPE.INCOME, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)
    expenses = Ledger(parent=userledger, title=u'Expenses', description=u'All expenses', placeholder=True, ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)
    equity = Ledger(parent=userledger, title=u'Equity', description=u'Financial infusions', placeholder=True, ltype=LEDGER_TYPE.EQUITY, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)

    db.session.add(assets)
    db.session.add(liabilities)
    db.session.add(income)
    db.session.add(expenses)
    db.session.add(equity)

    cash = Ledger(parent=assets, title=u'Cash', description=u'Cash in my wallet', ltype=LEDGER_TYPE.ASSET, lsubtype=LEDGER_SUBTYPE.CASH, currency=currency)
    bank = Ledger(parent=assets, title=u'Bank', description=u'My bank account', ltype=LEDGER_TYPE.ASSET, lsubtype=LEDGER_SUBTYPE.BANK, currency=currency)

    db.session.add(cash)
    db.session.add(bank)

    creditcard = Ledger(parent=liabilities, title=u'Credit Card', description=u'My credit cards', ltype=LEDGER_TYPE.LIABILITY, lsubtype=LEDGER_SUBTYPE.CREDITCARD, currency=currency)

    db.session.add(creditcard)

    salary = Ledger(parent=income, title=u'Salary', description=u'Income from current and previous employers', ltype=LEDGER_TYPE.INCOME, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)
    hobbies = Ledger(parent=income, title=u'Hobbies', description=u'Income from hobbies', ltype=LEDGER_TYPE.INCOME, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)
    gifts = Ledger(parent=income, title=u'Gifts', description=u'Cash gifts', ltype=LEDGER_TYPE.INCOME, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)

    db.session.add(salary)
    db.session.add(hobbies)
    db.session.add(gifts)

    rent = Ledger(parent=expenses, title=u'Rent', description=u'Monthly house rent', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)
    emi = Ledger(parent=expenses, title=u'EMI', description=u'Monthly payments for the house and car', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)
    food = Ledger(parent=expenses, title=u'Food', description=u'Breakfast, lunch and dinner', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)
    shopping = Ledger(parent=expenses, title=u'Shopping', description=u'All purchases', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)

    db.session.add(rent)
    db.session.add(emi)
    db.session.add(food)
    db.session.add(shopping)

    opening = Ledger(parent=equity, title=u'Opening Balances', ltype=LEDGER_TYPE.EXPENSE, lsubtype=LEDGER_SUBTYPE.NA, currency=currency)

    db.session.add(opening)
