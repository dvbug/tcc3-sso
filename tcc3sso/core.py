# coding:utf-8
"""
    tcc3sso.core
    ~~~~~~~~~~~~~~~~~~~~

    tcc3sso core module.
    :copyright: (c) 2015 by Vito.
    :license: GNU, see LICENSE for more details.
"""
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, UserMixin, AnonymousUserMixin
from mongoengine.queryset.visitor import Q

db = MongoEngine()
lm = LoginManager()
