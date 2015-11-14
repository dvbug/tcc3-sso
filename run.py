# coding:utf-8
"""
    run
    ~~~~~~~~~~~~~~~~~~~~

    tcc3sso run
    :copyright: (c) 2015 by Vito.
    :license: GNU, see LICENSE for more details.
"""

from tcc3sso import create_app

if __name__ == '__main__':
    app = create_app()
    app.run("0.0.0.0", 9001, debug=True)
