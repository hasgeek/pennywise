# -*- coding: utf-8 -*-

from datetime import datetime
from coaster import newid
from . import db
from .ledger import Ledger
from .commodity import Commodity

__all__ = ['Transaction', 'TransactionSplit']


class Transaction(db.Model):
    """
    Transaction between ledgers. Not to be confused with database transactions.
    """
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    #: Transaction UUID as a 22-char Base64 representation
    buid = db.Column(db.String(22), nullable=False, default=newid)
    #: Transaction date and time in UTC timezone
    datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    #: User-facing transaction id number
    num = db.Column(db.Unicode(30), nullable=False, default=u'')
    #: User description of transaction
    description = db.Column(db.Unicode(250), nullable=False, default=u'')
    commodity_id = db.Column(None, db.ForeignKey('commodity.id'), nullable=False)
    #: Commodity (usually currency) that this transaction is in
    commodity = db.relation(Commodity, primaryjoin=commodity_id == Commodity.id)
    #: Transactions may be disabled while speculating on expenses.
    #: Disabled transactions don't add to the balance
    disabled = db.Column(db.Boolean, default=False, nullable=False)

    def validate(self):
        """
        Assert that this transaction is well defined and safe to commit to database.
        """
        assert len(self.splits) > 1
        assert sum([s.value for s in self.splits]) == 0  # TODO: What about multi-currency?


class TransactionSplit(db.Model):
    """
    Transaction split, connecting a transaction to a ledger. Each split has a
    :attr:`value` specified in the primary commodity of the transaction. The
    sum of all split values always equals zero. If the split connects to a
    ledger with a different commodity, :attr:`quantity` is the exchange value.
    """
    __tablename__ = 'transaction_split'
    id = db.Column(db.Integer, primary_key=True)
    ledger_id = db.Column(None, db.ForeignKey('ledger.id'), nullable=False)
    #: Ledger that this split belongs to
    ledger = db.relation(Ledger, primaryjoin=ledger_id == Ledger.id,
        backref=db.backref('splits', order_by=id,
            cascade='all, delete-orphan'))
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    #: Transaction that this split belongs to
    transaction = db.relation(Transaction, primaryjoin=transaction_id == Transaction.id,
        backref=db.backref('splits', order_by=id,
            cascade='all, delete-orphan'))
    #: Has this transaction been reconciled within this ledger?
    reconciled = db.Column(db.Boolean, default=False, nullable=False)
    #: Date of reconciliation
    reconciled_date = db.Column(db.DateTime, nullable=True)
    #: Value of transaction
    value = db.Column(db.Numeric(20, 3), nullable=False)
    #: Quantity of transaction (same as value, except for cross-currency transactions)
    quantity = db.Column(db.Numeric(20, 3), nullable=False)
