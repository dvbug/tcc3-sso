# coding:utf-8
"""
    tcc3sso.sso.cookie
    ~~~~~~~~~~~~~~~~~~~~

    sso cookie module.
"""
import hashlib
import urllib.parse
from flask import request, url_for
from . import SSOToken
from ..helpers import get_referrer_name, get_referrer_url


class Cookie(object):
    security_validation_key = str(hashlib.md5('TCC3SSO'.encode(encoding='utf8')).hexdigest())
    form_auth_cookie_name = 'TCC3SSO.Security'
    auth_ticket_data_delimiter = '|'

    def __init__(self, token_id=None):
        self._cookie_value = None
        self.token_id = None

        if token_id is not None:
            self.init_cookie(token_id)

    def init_cookie(self, token_id):
        self.token_id = token_id
        self._cookie_value = Cookie.security_validation_key + Cookie.auth_ticket_data_delimiter + token_id

    @property
    def cookie_value(self):
        return self._cookie_value

    @classmethod
    def check(cls):
        if request.method == 'GET':
            referrer_name = get_referrer_name()
            referrer_url = get_referrer_url()
            print('check : ', referrer_url)
            if referrer_url.strip():
                token_id = Cookie.check_login()
                print('token_id', token_id)
                if token_id:
                    if len(token_id) == 0:
                        raise ValueError()
                    else:
                        token = SSOToken.validate_token_id(token_id)
                        if token:
                            ticket = token.add_new_ticket()
                            print('ticket', ticket)
                            if not isinstance(ticket, str):
                                raise TypeError('Incorrect data type for ticket.')

                            dic = {'ticket': ticket}
                            if referrer_url.find('?') >= 0:
                                split_chr = '&'
                            else:
                                split_chr = '?'

                            refer_url = referrer_url + split_chr + urllib.parse.urlencode(dic)
                            return refer_url

                # dic = {referrer_name: ('/sso?{}={}'.format(referrer_name, referrer_url))}
                # login_url = '/login?{}'.format(urllib.parse.urlencode(dic))
                dic = {referrer_name: referrer_url}
                refer_url = url_for('sso.login', **dic)
                return refer_url
            else:
                url = ''
                return url

    @classmethod
    def check_login(cls):
        auth_cookie = request.cookies.get(Cookie.form_auth_cookie_name)
        if auth_cookie:
            if type(auth_cookie) == str:
                delimiter_pos = auth_cookie.find(Cookie.auth_ticket_data_delimiter)
                if delimiter_pos >= 0:
                    security_str = auth_cookie[:delimiter_pos]
                    if security_str == Cookie.security_validation_key:
                        token = auth_cookie[(delimiter_pos + 1):]
                        return token
        return None

