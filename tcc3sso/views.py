# coding:utf-8
"""
    tcc3sso.views
    ~~~~~~~~~~~~~~~~~~~~

    tcc3sso views module.
    :copyright: (c) 2015 by Vito.
    :license: GNU, see LICENSE for more details.
"""
import urllib.parse
from flask import Blueprint, abort, render_template, url_for, make_response, redirect, flash, request, jsonify
from .forms import LoginForm, SignupForm
from .sso import LoginUser, SSOToken, Cookie, SSOApi
from .helpers import get_referrer_url, get_referrer_name
from .settings import CURRENT_API

bp_main = Blueprint('main', __name__)
bp_sso = Blueprint('sso', __name__, url_prefix='/sso')
bp_api = Blueprint('api', __name__, url_prefix='/api')
bp_api_1_0 = Blueprint('api_1_0', __name__, url_prefix='/api/v1.0')


def get_referrer_dict():
    referrer_name = get_referrer_name()
    referrer_url = get_referrer_url()
    vals = {referrer_name: referrer_url}
    return referrer_name, referrer_url, vals


# When accessing a web root directory,
# if there is a referrer parameters,
# then redirected to the login page
@bp_main.route('/')
def root():
    _, referrer_url, referrer_dict = get_referrer_dict()

    if referrer_url:
        redirect_url = url_for('sso.sso', **referrer_dict)
    else:

        redirect_url = url_for('main.index', **referrer_dict)
    print('main root redirect_url:', redirect_url)
    return redirect(redirect_url)


@bp_main.route('/index')
def index():
    _, _, referrer_dict = get_referrer_dict()
    return render_template('index.html', referrer_dict=referrer_dict)


@bp_sso.route('/')
def sso():
    try:
        referrer_url = Cookie.check()
        print('Cookie.check url: {}'.format(referrer_url))
        return redirect(referrer_url)
    except ValueError:
        abort(404)


@bp_sso.route('/login', methods=['GET', 'POST'])
def login():
    _, referrer_url, referrer_dict = get_referrer_dict()
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = LoginUser.query_user(form.account.data, form.pwd.data)
            if not user:
                raise ValueError('The account or the password is incorrect.')

            # login_user(user)

            token = SSOToken(user.name)
            SSOToken.add_token(token)
            ticket = token.add_new_ticket()
            if not isinstance(ticket, str):
                raise TypeError('Incorrect data type for ticket.')

            dic = {'ticket': ticket}
            if referrer_url.find('?') >= 0:
                split_chr = '&'
            else:
                split_chr = '?'

            referrer_url = referrer_url + split_chr + urllib.parse.urlencode(dic)
            cookie_value = Cookie(token.id).cookie_value

            print('login POST referrer_url: {}'.format(referrer_url))
            if not referrer_url.strip():
                # referrer_url = '/error'
                return redirect(url_for('main.index'))

            resp = make_response(redirect(referrer_url))
            resp.set_cookie(Cookie.form_auth_cookie_name, cookie_value)
            print('login POST resp: {}'.format(resp))
            return resp

    except ValueError:
        abort(401)

    return render_template('login.html', form=form, referrer_dict=referrer_dict)


@bp_sso.route('/register', methods=['POST', 'GET'])
def register():
    _, _, referrer_dict = get_referrer_dict()
    print('sso.register:', referrer_dict)
    form = SignupForm()
    if form.validate_on_submit():
        if LoginUser.register_user(form.nick_name.data, form.pwd.data, form.email.data, description='User'):
            flash('Sign up success,Please Login.')
            return redirect(url_for('sso.login'))
    return render_template('sign_up.html', form=form, referrer_dict=referrer_dict)


@bp_sso.route('/logout/<string:user_name>', methods=['GET'])
def logout(user_name):
    try:
        token = SSOToken.find_by_user_name(user_name)
        if token:
            if SSOToken.remove_token(token):
                resp = make_response(redirect(request.referrer))
                resp.delete_cookie(Cookie.form_auth_cookie_name)
                return resp
    except ValueError:
        abort(401)


@bp_api.route('/ping', methods=['GET'])
def ping():
    token = request.args.get('token', '')
    return SSOApi.ping(token)


@bp_api.route('/validation', methods=['GET'])
def validation():
    if CURRENT_API and CURRENT_API['end_point'] is not None:
        ret_dict = {
            'api': url_for('{}.validate_ticket'.format(CURRENT_API['end_point']), ticket_id=''),
            'version': CURRENT_API['version']
        }
        return make_response(jsonify(ret_dict))
    else:
        ret_dict = {
            'error': 'No valid api version'
        }
        return make_response(jsonify(ret_dict), 400)


@bp_api_1_0.route('/validation/<ticket_id>', methods=['GET'])
def validate_ticket(ticket_id):
    return SSOApi.validate_ticket(ticket_id)



