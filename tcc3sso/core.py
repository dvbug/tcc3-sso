# coding:utf-8
"""
    tcc3sso.core
    ~~~~~~~~~~~~~~~~~~~~

    tcc3sso core module.
"""
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from mongoengine.queryset.visitor import Q

db = MongoEngine()
lm = LoginManager()
