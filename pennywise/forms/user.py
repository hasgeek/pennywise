# -*- coding: utf-8 -*-

from flaskext.wtf import Form, TextField, PasswordField, BooleanField, SelectField
from flaskext.wtf import Required, Email, EqualTo, ValidationError

from pennywise.models import User
from pennywise.data import currency_codes

class LoginForm(Form):
    username = TextField('Username or Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

    def getuser(self, name):
        if '@' in name:
            return User.query.filter_by(email=name).first()
        else:
            return User.query.filter_by(username=name).first()

    def validate_username(self, field):
        existing = self.getuser(field.data)
        if existing is None:
            raise ValidationError, "User does not exist"

    def validate_password(self, field):
        user = self.getuser(self.username.data)
        if user is None or not user.check_password(field.data):
            raise ValidationError, "Invalid password"
        self.user = user # XXX: Is this reasonable?


class RegisterForm(Form):
    username = TextField('Username', validators=[Required()])
    fullname = TextField('Full name', validators=[Required()])
    email = TextField('Email Address', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    confirm_password = PasswordField('Confirm Password',
                          validators=[Required(), EqualTo('password')])
    currency = SelectField('Default Currency', choices=currency_codes,
                          validators=[Required()])
    accept_rules = BooleanField('I accept the site rules', validators=[Required()])

    def validate_username(self, field):
        existing = User.query.filter_by(username=field.data).first()
        if existing is not None:
            raise ValidationError, "That username is taken"

    def validate_email(self, field):
        existing = User.query.filter_by(email=field.data).first()
        if existing is not None:
            raise ValidationError, "That email is already registered. Do you want to login?"

