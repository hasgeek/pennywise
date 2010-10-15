# -*- coding: utf-8 -*-

"""
Operations on ledgers.
"""

from pennywise.models import COMMODITY_TYPE, Commodity, db
from pennywise.data import currency_codes

def get_or_make_commodity(type, symbol, commit=False):
    """
    Return a Commodity for the given type and symbol. If not already in db,
    make and add, then return.
    """
    commodity = Commodity.query.filter_by(type=type, symbol=symbol).first()
    if commodity is None:
        if type == COMMODITY_TYPE.CURRENCY:
            # Iterate through currency_codes looking for commodity
            name = None
            for ccode, cname in currency_codes:
                if symbol == ccode:
                    name = cname
                    break
        if name:
            commodity = Commodity(type=type, symbol=symbol, name=name)
            db.session.add(commodity)
    if commit:
        db.session.commit()
    return commodity
