# coding:utf-8
"""
    tcc3sso.sso.api
    ~~~~~~~~~~~~~~~~~~~~

    tcc3sso sso api module.
    :copyright: (c) 2015 by Vito.
    :license: GNU, see LICENSE for more details.
"""
from flask import make_response, jsonify
from .token import SSOToken


class SSOApi(object):
    PING_TOKEN = 'TCCSSOC'

    @classmethod
    def validate_ticket(cls, ticket_id):
        ret = SSOToken.validate_ticket(ticket_id)
        if ret is not None:
            token = ret[0]
            ticket = ret[1]

            validate_result = {
                'valid': True,
                'user': token.user_name,
                'newticket': ticket
            }

            return make_response(jsonify(validate_result))
        else:
            validate_result = {
                'valid': False
            }
            return make_response(jsonify(validate_result))

    @classmethod
    def ping(cls, token):
        if token is not None:
            if isinstance(token, str):
                if token == SSOApi.PING_TOKEN:
                    return make_response('OK')
        return make_response('NG', 400)
