# -*- coding: utf-8 -*-
# Copyright (C) 2010, Kiran Jonnalagadda. All rights reserved.

import uuid
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Unicode, UnicodeText, Integer
from sqlalchemy import Boolean, SmallInteger, Numeric, DateTime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relation, backref, scoped_session, sessionmaker
from sqlalchemy.orm import Query

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

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

class Ledger(Base):
    """
    Ledger containing transactions with other ledgers.
    """
    __tablename__ = 'ledger'
    id = Column(Integer, primary_key=True)
    #: Location of ledger. Local or foreign
    location = Column(String(20), nullable=False)
    __mapper_args__ = {'polymorphic_on': location, 'polymorphic_identity': 'local'}
    #: URL name of ledger. Must be site-unique and permanent
    name = Column(Unicode(50), default=makeuuid, unique=True, nullable=False)
    #: Title of ledger
    title = Column(Unicode(50), nullable=False)
    #: User code for ledger
    code = Column(Unicode(50), default='', nullable=False)
    #: Single-line description for ledger
    description = Column(Unicode(250), default='', nullable=False)
    #: Longer text about this ledger
    notes = Column(UnicodeText, default='', nullable=False)
    #: Placeholder ledgers can't contain transactions. They're meant
    #: for holding a place in a hierarchy
    placeholder = Column(Boolean, default=False, nullable=False)
    #: Hidden ledgers are hidden in the UI.
    hidden = Column(Boolean, default=False, nullable=False)
    #: Ledger type
    ltype = Column('type', SmallInteger, nullable=False)
    #: Ledger sub-type, if applicable. Affects UI
    lsubtype = Column('subtype', SmallInteger, default=LEDGER_SUBTYPE.NA, nullable=False)
    #: Currency of ledger
    currency = Column(Unicode(3), default='', nullable=False)
    #: Ledger's parent, for nested ledgers
    parent_id = Column(Integer, ForeignKey('ledger.id'), nullable=True)
    #: SQLAlchemy mapper to access parent ledger object
    parent = relation('Ledger', foreign_keys=parent_id,
                      backref=backref('subledgers', order_by=name,
                                      cascade="all, delete-orphan"))
    #: Current balance in ledger
    balance = Column(Numeric, nullable=False, default=0)

    query = DBSession.query_property(Query)

    def __init__(self, **kw):
        # Balance on new ledgers is always zero
        kw['balance'] = 0
        super(Ledger, self).__init__(**kw)

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


class ForeignLedger(Ledger):
    """
    Placeholder for a remotely-hosted ledger. These ledgers are hidden by
    default and do not have a known balance.
    """
    __tablename__ = 'foreignledger'
    __mapper_args__ = {'polymorphic_identity': 'foreign'}
    id = Column(Integer, ForeignKey('ledger.id'), primary_key=True)
    #: Remote location of this ledger, as a valid URL
    url = Column(Unicode(250), nullable=False)

    def __init__(self, **kw):
        kw['hidden'] = True
        kw['ltype'] = LEDGER_TYPE.USER
        super(ForeignLedger, self).__init__(**kw)


class UserLedger(Ledger):
    """
    Base ledger for all of a user's ledgers. Always a placeholder.
    """
    __tablename__ = 'userledger'
    __mapper_args__ = {'polymorphic_identity': 'user'}
    id = Column(Integer, ForeignKey('ledger.id'), primary_key=True)
    
    def __init__(self, **kw):
        kw['placeholder'] = True
        super(UserLedger, self).__init__(**kw)


class Transaction(Base):
    """
    Transaction between ledgers. Not to be confused with database transactions.
    """
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    #: Transaction UUID as a 36-char string representation
    uuid = Column(String(36), nullable=False, default=makeuuid)
    #: Transaction date and time in UTC timezone
    datetime = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    #: User-facing transaction id number
    num = Column(Unicode(30), nullable=False, default='')
    #: User description of transaction
    description = Column(Unicode(250), nullable=False, default='')
    #: This is a cross-currency transaction
    crosscurrency = Column(Boolean, default=False, nullable=False)
    #: Exchange rate for two-currency transactions. Mutually exclusive with
    #: :attr:`exchangevalue`.
    exchangerate = Column(Numeric, nullable=False)
    #: Exchange value for two-currency transactions. Mutually exclusive with
    #: :attr:`exchangerate'.
    exchangevalue = Column(Numeric, nullable=True)

    query = DBSession.query_property(Query)


class TransactionSplit(Base):
    """
    Transaction split, connecting a transaction to a ledger.
    """
    __tablename__ = 'transactionsplit'
    id = Column(Integer, primary_key=True)
    #: Ledger that this split belongs to
    ledger_id = Column(Integer, ForeignKey('ledger.id'), nullable=False)
    #: SQLAlchemy mapper to load ledger object
    ledger = relation(Ledger, primaryjoin=ledger_id == Ledger.id,
                      backref=backref('splits', order_by=id,
                                      cascade='all, delete-orphan'))
    #: Transaction that this split belongs to
    transaction_id = Column(Integer, ForeignKey('transaction.id'), nullable=False)
    #: SQLALchemy mapper to load transaction object
    transaction = relation(Transaction, primaryjoin=transaction_id == Transaction.id,
                           backref=backref('splits', order_by=id,
                                           cascade='all, delete-orphan'))
    #: Has this transaction been reconciled within this ledger?
    reconciled = Column(Boolean, default=False, nullable=False)
    #: Value of transaction
    value = Column(Numeric, nullable=False)

    query = DBSession.query_property(Query)

__all__ = [LEDGER_TYPE, LEDGER_SUBTYPE, LEDGER_TYPE_COMBOS,
           Ledger, ForeignLedger, Transaction, TransactionSplit,
           IntegrityError, NoResultFound]
