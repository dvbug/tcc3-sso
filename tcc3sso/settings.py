# coding:utf-8
"""
    tcc3sso.settings
    ~~~~~~~~~~~~~~~~~~~~

    tcc3sso settings config.
"""

CSRF_ENABLED = True
SECRET_KEY = 'this-is-a-secret'

MONGODB_SETTINGS = {
    'db': 'tccdevdb',
    'host': '192.168.1.91',
    'port': 20000
}

CURRENT_API = {
    'end_point': 'api_1_0',
    'version': 'v1.0',
}


REFERRER_NAME = 'url'
