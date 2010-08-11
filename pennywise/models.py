# -*- coding: utf-8 -*-

import uuid
import datetime

from pennywise import app
from pennywise.data import currency_symbols
from flaskext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

# ----------------------------------------------------------------------------
# Constants

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


# ----------------------------------------------------------------------------
# Helper functions

def makeuuid():
    return str(uuid.uuid4())


# ----------------------------------------------------------------------------
# Declarative tables

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.Unicode(80))
    username = db.Column(db.Unicode(80), unique=True, nullable=True)
    email = db.Column(db.Unicode(80), unique=True, nullable=True)
    openid = db.Column(db.Unicode(200), unique=True, nullable=True)
    pw_hash = db.Column(db.String(80))

    def __init__(self, password=None, **kwargs):
        self.password = password
        super(User, self).__init__(**kwargs)

    def _set_password(self, password):
        if password is None:
            self.pw_hash = None
        else:
            self.pw_hash = generate_password_hash(password)

    password = property(fset=_set_password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return '<User %r>' % (self.username or self.email or self.openid)


class Ledger(db.Model):
    """
    Ledger containing transactions with other ledgers.
    """
    __tablename__ = 'ledger'
    id = db.Column(db.Integer, primary_key=True)
    #: Location of ledger. Local or foreign
    location = db.Column(db.String(20), nullable=False)
    __mapper_args__ = {'polymorphic_on': location, 'polymorphic_identity': 'ledger'}
    #: URL name of ledger. Must be site-unique and permanent
    uuid = db.Column(db.Unicode(50), default=makeuuid,
                     unique=True, nullable=False)
    #: Title of ledger
    title = db.Column(db.Unicode(50), nullable=False)
    #: User code for ledger
    code = db.Column(db.Unicode(50), default='', nullable=False)
    #: Single-line description for ledger
    description = db.Column(db.Unicode(250), default='', nullable=False)
    #: Longer text about this ledger
    notes = db.Column(db.UnicodeText, default='', nullable=False)
    #: Placeholder ledgers can't contain transactions. They're meant
    #: for holding a place in a hierarchy
    placeholder = db.Column(db.Boolean, default=False, nullable=False)
    #: Hidden ledgers are hidden in the UI.
    hidden = db.Column(db.Boolean, default=False, nullable=False)
    #: Ledger type
    ltype = db.Column('type', db.SmallInteger, nullable=False)
    #: Ledger sub-type, if applicable. Affects UI
    lsubtype = db.Column('subtype', db.SmallInteger,
                         default=LEDGER_SUBTYPE.NA, nullable=False)
    #: Currency of ledger
    currency = db.Column(db.Unicode(3), default='', nullable=False)
    #: Ledger's parent, for nested ledgers
    parent_id = db.Column(db.Integer, db.ForeignKey('ledger.id'), nullable=True)
    #: SQLAlchemy mapper to access parent ledger object
    parent = db.relation('Ledger', remote_side=[id], backref=db.backref('subledgers', order_by=title))
    #: Current balance in ledger
    balance = db.Column(db.Numeric, nullable=False, default=0)

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

    def formatted_balance(self):
        """
        Return balance as a formatted string.
        """
        return '%s %.2f' % (currency_symbols.get(self.currency, self.currency), self.balance)


class ForeignLedger(Ledger):
    """
    Placeholder for a remotely-hosted ledger. These do not have a known
    balance. ForeignLedgers are not yet supported.
    """
    __tablename__ = 'foreignledger'
    __mapper_args__ = {'polymorphic_identity': 'foreignledger'}
    id = db.Column(db.Integer, db.ForeignKey('ledger.id'), primary_key=True)
    #: Remote location of this ledger, as a valid URL
    remoteurl = db.Column(db.Unicode(250), nullable=False)

    def __init__(self, **kwargs):
        kwargs['ltype'] = LEDGER_TYPE.USER
        super(ForeignLedger, self).__init__(**kwargs)


class UserLedger(Ledger):
    """
    Base ledger for all of a user's ledgers. Always a placeholder.
    """
    __tablename__ = 'userledger'
    __mapper_args__ = {'polymorphic_identity': 'userledger'}
    id = db.Column(db.Integer, db.ForeignKey('ledger.id'), primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    #: Owner of this ledger
    owner = db.relation('User', foreign_keys=owner_id, uselist=False,
                        backref=db.backref('ledger',
                                           cascade='all, delete-orphan', uselist=False))

    def __init__(self, **kwargs):
        kwargs['placeholder'] = True
        if 'parent' in kwargs:
            del kwargs['parent']
        kwargs['parent_id'] = None
        kwargs['ltype'] = LEDGER_TYPE.USER
        kwargs['lsubtype'] = LEDGER_SUBTYPE.NA
        super(UserLedger, self).__init__(**kwargs)

    @db.validates('parent')
    def validate_parent(self, key, value):
        assert value is None
        return None

    @db.validates('placeholder')
    def validate_placeholder(self, key, value):
        assert value is True
        return True

    @db.validates('ltype')
    @db.validates('lsubtype')
    def validate_type(self, key, value):
        assert (key, value) in [('ltype', LEDGER_TYPE.USER), ('lsubtype', LEDGER_SUBTYPE.NA)]
        return value


class LedgerAccess(db.Model):
    """
    Access rights to ledgers.
    """
    __tablename__ = 'ledgeraccess'
    ledger_id = db.Column(db.Integer, db.ForeignKey('ledger.id'), primary_key=True)
    #: Ledger that this permission applies to
    ledger = db.relation('Ledger', foreign_keys=ledger_id,
                            backref=db.backref('users', cascade='all, delete-orphan'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    #: User that this permission applies to
    user = db.relation('User', foreign_keys=user_id,
                       backref=db.backref('ledgers', cascade='all, delete-orphan'))
    #: Can this user view the ledgers and transactions in this ledger?
    can_read = db.Column(db.Boolean, default=True, nullable=False)
    #: Can this user make new transactions in this ledger?
    can_write = db.Column(db.Boolean, default=False, nullable=False)
    #: Can this user edit other users' transactions in this ledger?
    can_write_all = db.Column(db.Boolean, default=False, nullable=False)


class Transaction(db.Model):
    """
    Transaction between ledgers. Not to be confused with database transactions.
    """
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    #: Transaction UUID as a 36-char string representation
    uuid = db.Column(db.String(36), nullable=False, default=makeuuid)
    #: Transaction date and time in UTC timezone
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    #: User-facing transaction id number
    num = db.Column(db.Unicode(30), nullable=False, default='')
    #: User description of transaction
    description = db.Column(db.Unicode(250), nullable=False, default='')
    #: Transactions may be disabled while speculating on expenses
    disabled = db.Column(db.Boolean, default=False, nullable=False)
    #: This is a cross-currency transaction
    crosscurrency = db.Column(db.Boolean, default=False, nullable=False)
    #: Exchange rate for two-currency transactions. Mutually exclusive with
    #: :attr:`exchangevalue`.
    exchangerate = db.Column(db.Numeric, nullable=False)
    #: Exchange value for two-currency transactions. Mutually exclusive with
    #: :attr:`exchangerate`.
    exchangevalue = db.Column(db.Numeric, nullable=True)

    def validate(self):
        """
        Assert that this transaction is well defined and safe to commit to database.
        """
        assert len(self.splits) > 1
        assert sum([s.value for s in self.splits]) == 0 # TODO: What about multi-currency?


class TransactionSplit(db.Model):
    """
    Transaction split, connecting a transaction to a ledger.
    """
    __tablename__ = 'transactionsplit'
    id = db.Column(db.Integer, primary_key=True)
    #: Ledger that this split belongs to
    ledger_id = db.Column(db.Integer, db.ForeignKey('ledger.id'), nullable=False)
    #: SQLAlchemy mapper to load ledger object
    ledger = db.relation(Ledger, primaryjoin=ledger_id == Ledger.id,
                      backref=db.backref('splits', order_by=id,
                                      cascade='all, delete-orphan'))
    #: Transaction that this split belongs to
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    #: SQLALchemy mapper to load transaction object
    transaction = db.relation(Transaction, primaryjoin=transaction_id == Transaction.id,
                           backref=db.backref('splits', order_by=id,
                                           cascade='all, delete-orphan'))
    #: Has this transaction been reconciled within this ledger?
    reconciled = db.Column(db.Boolean, default=False, nullable=False)
    #: Value of transaction
    value = db.Column(db.Numeric, nullable=False)

__all__ = ['db',
           'LEDGER_TYPE', 'LEDGER_SUBTYPE', 'LEDGER_TYPE_COMBOS',
           'Ledger', 'ForeignLedger', 'UserLedger', 'Transaction',
           'TransactionSplit']
