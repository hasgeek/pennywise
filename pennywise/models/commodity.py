# -*- coding: utf-8 -*-

from . import db
from .data import currency_codes

__all__ = ['COMMODITY_TYPE', 'Commodity']


class COMMODITY_TYPE:
    #: A cash currency
    CURRENCY = 0
    #: A traded stock (symbol will be NYSE:AAPL, etc)
    STOCK = 1
    #: A mutual fund (TODO: figure out symbols/names)
    FUND = 2


# TODO: Can commodities be user-defined? Can Pennywise
# be used as an inventory tracker?
class Commodity(db.Model):
    """
    Commodities (currencies, funds, etc)
    """
    __tablename__ = 'commodity'
    id = db.Column(db.Integer, primary_key=True)
    #: Type of commodity
    type = db.Column(db.SmallInteger, nullable=False, default=COMMODITY_TYPE.CURRENCY)
    symbol = db.Column(db.Unicode(20), nullable=False)
    title = db.Column(db.Unicode(250), nullable=False, default=u'')

    @classmethod
    def get_or_create(cls, type, symbol, title=u''):
        commodity = cls.query.filter_by(type=type, symbol=symbol).first()
        if commodity is None:
            if type == COMMODITY_TYPE.CURRENCY:
                # Iterate through currency_codes looking for commodity
                for ccode, cname in currency_codes:
                    if symbol == ccode:
                        title = cname
                        break
            commodity = Commodity(type=type, symbol=symbol, title=title)
        return commodity
