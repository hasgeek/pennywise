# -*- coding: utf-8 -*-

from . import db, NodeMixin, Node
from .commodity import Commodity

__all__ = ['LEDGER_TYPE', 'LEDGER_SUBTYPE', 'TRANSFER_COLUMNS', 'Ledger']


class LEDGER_TYPE:
    USER = 0
    ASSET = 1
    LIABILITY = 2
    INCOME = 3
    EXPENSE = 4
    EQUITY = 5


class LEDGER_SUBTYPE:
    NA = 0
    BANK = 1
    CASH = 2
    CREDITCARD = 3
    ACC_RECEIVABLE = 4
    ACC_PAYABLE = 5

# TODO: Make this a dictionary. More effective for look-ups
LEDGER_TYPE_COMBOS = set([
    (LEDGER_TYPE.USER, LEDGER_SUBTYPE.NA),
    (LEDGER_TYPE.ASSET, LEDGER_SUBTYPE.NA),
    (LEDGER_TYPE.ASSET, LEDGER_SUBTYPE.BANK),
    (LEDGER_TYPE.ASSET, LEDGER_SUBTYPE.CASH),
    (LEDGER_TYPE.LIABILITY, LEDGER_SUBTYPE.NA),
    (LEDGER_TYPE.LIABILITY, LEDGER_SUBTYPE.CREDITCARD),
    (LEDGER_TYPE.LIABILITY, LEDGER_SUBTYPE.ACC_PAYABLE),
    (LEDGER_TYPE.INCOME, LEDGER_SUBTYPE.NA),
    (LEDGER_TYPE.INCOME, LEDGER_SUBTYPE.ACC_RECEIVABLE),
    (LEDGER_TYPE.EXPENSE, LEDGER_SUBTYPE.NA),
    (LEDGER_TYPE.EQUITY, LEDGER_SUBTYPE.NA),
    ])

# TODO: Add Acc/receivable and payable, and cross-check signage

#: Ledger headers for debit, credit, and signage
#: These labels and signage are for personal accounts, as defined at
#: http://en.wikipedia.org/wiki/Debits_and_credits#Operational_Principles
TRANSFER_COLUMNS = {
    (LEDGER_TYPE.ASSET,     LEDGER_SUBTYPE.NA):         (u'Increase', u'Decrease',   +1),
    (LEDGER_TYPE.ASSET,     LEDGER_SUBTYPE.BANK):       (u'Deposit',  u'Withdrawal', +1),
    (LEDGER_TYPE.ASSET,     LEDGER_SUBTYPE.CASH):       (u'Receive',  u'Spend',      +1),
    (LEDGER_TYPE.LIABILITY, LEDGER_SUBTYPE.NA):         (u'Decrease', u'Increase',   -1),
    (LEDGER_TYPE.LIABILITY, LEDGER_SUBTYPE.CREDITCARD): (u'Payment',  u'Charge',     -1),
    (LEDGER_TYPE.INCOME,    LEDGER_SUBTYPE.NA):         (u'Charge',   u'Income',     -1),
    (LEDGER_TYPE.EXPENSE,   LEDGER_SUBTYPE.NA):         (u'Expense',  u'Rebate',     +1),
    (LEDGER_TYPE.EQUITY,    LEDGER_SUBTYPE.NA):         (u'Decrease', u'Increase',   -1),
    }


class Ledger(NodeMixin, Node):
    """
    Ledger containing transactions with other ledgers.
    """
    __tablename__ = 'ledger'
    #: User code for ledger
    code = db.Column(db.Unicode(50), default=u'', nullable=False)
    #: Single-line description for ledger
    description = db.Column(db.Unicode(250), default=u'', nullable=False)
    #: Longer text about this ledger
    notes = db.Column(db.UnicodeText, default=u'', nullable=False)
    #: Placeholder ledgers can't contain transactions. They're meant
    #: for holding a place in a hierarchy
    placeholder = db.Column(db.Boolean, default=False, nullable=False)
    #: Hidden ledgers are hidden in the UI.
    hidden = db.Column(db.Boolean, default=False, nullable=False)
    #: Ledger type
    ledger_type = db.Column(db.SmallInteger, nullable=False)
    #: Ledger sub-type, if applicable. Affects UI
    ledger_subtype = db.Column(db.SmallInteger,
        default=LEDGER_SUBTYPE.NA, nullable=False)
    #: Commodity of ledger
    commodity_id = db.Column(None, db.ForeignKey('commodity.id'), nullable=False)
    commodity = db.relation(Commodity, primaryjoin=commodity_id == Commodity.id)
    #: Current balance in ledger.
    balance = db.Column(db.Numeric(20, 3), nullable=False, default='0')

    def __repr__(self):
        return u"<Ledger '%s'>" % self.title

    def __init__(self, **kwargs):
        # Balance on new ledgers is always zero
        kwargs['balance'] = 0
        super(Ledger, self).__init__(**kwargs)

    def addSplitValue(self, split):
        """
        Update ledger balance given a new split.
        """
        self.balance += split.value

    def delSplitValue(self, split):
        """
        Update ledger balance for a split being removed.
        """
        self.balance -= split.value
