# coding:utf-8
"""
    wsgi
    ~~~~

    tcc3sso wsgi interface.
    :copyright: (c) 2015 by Vito.
    :license: GNU, see LICENSE for more details.
"""

from tcc3sso import create_app, settings_override

application = create_app(settings_override=settings_override)


if __name__ == '__main__':
    application.run("0.0.0.0", 9001, debug=True)
