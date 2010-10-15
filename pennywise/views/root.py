# -*- coding: utf-8 -*-

from flask import redirect, url_for, g, session, render_template, flash
from pennywise import app
from pennywise.models import db, User, UserLedger
from pennywise.commodities import COMMODITY_TYPE, get_or_make_commodity
from pennywise.forms.user import LoginForm, RegisterForm
from pennywise.ledgers import make_default_ledgers


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
@app.route('/favicon.ico/')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'), code=301)


@app.route('/login/', methods=['GET'])
def loginform():
    form = LoginForm()
    return render_template('form.html', form=form)


@app.route('/login/', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user
        g.user = user
        session['username'] = user.username
        flash('You are now logged in', category='info')
        return redirect(url_for('userpage', username=user.username), code=303)
    else:
        flash('Please try again', category='error')
        return render_template('form.html', form=form)


@app.route('/logout/')
def logout():
    g.user = None
    del session['username']
    flash('You are now logged out', category='info')
    return redirect(url_for('index'), code=303)


@app.before_request
def lookup_current_user():
    g.user = None
    if 'username' in session:
        g.user = User.query.filter_by(username=session['username']).first()


@app.route('/register', methods=['GET'])
def registerform():
    form = RegisterForm()
    return render_template('form.html', form=form)


@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        # Make a ledger for the user
        currency = form.currency.data
        commodity = get_or_make_commodity(type=COMMODITY_TYPE.CURRENCY, symbol=currency, commit=False)
        ledger = UserLedger(owner=user, title='', commodity=commodity)
        db.session.add(ledger)
        # Make some default ledgers
        make_default_ledgers(ledger)
        db.session.commit()
        g.user = user # Not really required since we're not rendering a page
        session['username'] = user.username
        flash('Yay! You are now one of us. Welcome aboard!', category='info')
        return redirect(url_for('userpage', username=user.username), code=303)
    else:
        flash('Your form contained errors.', category='error')
        return render_template('form.html', form=form)
