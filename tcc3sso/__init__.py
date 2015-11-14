# coding:utf-8
"""
    tcc3sso
    ~~~~~~~~~~~~~~~~~~~~

    tcc3sso package.
    :copyright: (c) 2015 by Vito.
    :license: GNU, see LICENSE for more details.
"""
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from .views import bp_sso, bp_main, bp_api, bp_api_1_0
from .core import db, lm
from .helpers import JSONEncoder
from .sso.entities import LoginUser


def create_app(settings_override=None):
    """Returns a :class:`Flask` application instance.
    :param settings_override: a dictionary of settings to override.
    :return: Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.json_encoder = JSONEncoder
    app.config.from_object("tcc3sso.settings")
    app.config.from_object(settings_override)

    # something need init
    db.init_app(app)
    lm.init_app(app)
    Bootstrap(app)

    @lm.user_loader
    def load_user(user_id):
        user = LoginUser.objects.get(id=user_id)
        return user

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_sso)
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_api_1_0)

    for e in [500, 404]:
        app.errorhandler(e)(handle_error)

    return app


def handle_error(e):
    return render_template('errors/%s.html' % e.code), e.code
