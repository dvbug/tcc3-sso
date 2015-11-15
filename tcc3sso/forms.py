# coding:utf-8
"""
    tcc3sso.forms
    ~~~~~~~~~~~~~~~~~~~~

    tcc3sso forms module.
    :copyright: (c) 2015 by Vito.
    :license: GNU, see LICENSE for more details.
"""
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, ValidationError, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from .sso.entities import GENDER_LIST


def pwd_length_check(form, field):
    if len(field.data) > 16:
        raise ValidationError('Filed must be less than 16 characters.')

    if not field.data.isalnum():
        raise ValidationError('Password should only contains alphabets or digits')

    if field.data.isalpha() or field.data.isdigit():
        raise ValidationError('Password should contains both alphabets and digits')


def name_input_check(form, field):
    if len(field.data) > 24:
        raise ValidationError('Filed must be less than 24 characters.')

    if not field.data.isalnum():
        raise ValidationError('Username should only contains alphabets or digits')


class LoginForm(Form):
    account = StringField('account', validators=[DataRequired()])  # , name_input_check
    pwd = PasswordField('pwd', validators=[DataRequired(), pwd_length_check])


class SignupForm(Form):
    nick_name = StringField('nick name', validators=[DataRequired(), name_input_check])
    pwd = PasswordField('pwd', validators=[DataRequired(),
                                           Length(4, 16, message='password must be between 4 and 16 characters.')])
    cfm_pwd = PasswordField('cfm pwd', validators=[DataRequired(), EqualTo('pwd')])
    email = StringField('email', validators=[DataRequired(), Email()])
    cfm_email = StringField('cfm email', validators=[DataRequired(), EqualTo('email')])

    real_name = StringField('real name', validators=[name_input_check])
    # phones = StringField('phones', validators=[DataRequired(), name_input_check])
    birth = DateField('birth day', validators=[])
    gender = SelectField('gender', choices=GENDER_LIST)
    brief_description = \
        StringField('brief desc', validators=[
            Length(max=140, message='brief description must be less than 140 characters.')
        ])
