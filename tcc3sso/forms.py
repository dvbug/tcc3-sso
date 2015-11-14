# coding:utf-8
"""
    tcc3sso.forms
    ~~~~~~~~~~~~~~~~~~~~

    tcc3sso forms module.
"""
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo


def pwd_length_check(form, field):
    if len(field.data) > 16:
        raise ValidationError('Filed must be less than 16 characters.')

    if not field.data.isalnum():
        raise ValidationError('Password should only contains alphabets or digits')

    if field.data.isalpha() or field.data.isdigit():
        raise ValidationError('Password should contains both alphabets and digits')


def name_input_check(form, field):
    if len(field.data) > 16:
        raise ValidationError('Filed must be less than 16 characters.')

    if not field.data.isalnum():
        raise ValidationError('Username should only contains alphabets or digits')


class LoginForm(Form):
    account = StringField('account', validators=[DataRequired()])  # , name_input_check
    pwd = PasswordField('pwd', validators=[DataRequired(), pwd_length_check])


class SignupForm(Form):
    nick_name = StringField('nick_name', validators=[DataRequired(), name_input_check])
    pwd = PasswordField('pwd', validators=[DataRequired(), pwd_length_check])
    cfm_pwd = PasswordField('cfm_pwd', validators=[DataRequired(), EqualTo('pwd')])
    email = StringField('email', validators=[DataRequired(), Email()])
    cfm_email = StringField('cfm_email', validators=[DataRequired(), EqualTo('email')])
