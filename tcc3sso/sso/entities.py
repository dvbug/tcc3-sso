# coding:utf-8
"""
    tcc3sso.sso.entities
    ~~~~~~~~~~~~~~~~~~~~

    sso entities module.
"""

from ..core import db, Q


class LoginUser(db.Document):
    # 指定 mongo collection的名字
    meta = {'collection': 'user'}

    name = db.StringField(required=True, max_length=64)
    password = db.StringField(required=True, max_length=256)
    email = db.StringField(required=True, max_length=64)
    description = db.StringField(max_length=240)

    def __str__(self):
        return "name:{}".format(self.name)

    @classmethod
    def register_user(cls, nick_name, password, email, description=None):
        try:
            login_user = LoginUser(name=nick_name, password=password, email=email, description=description)
            login_user.save()
            return True
        except Exception as e:
            print("register user error:{}".format(e))
            return False

    @classmethod
    def query_user(cls, account, password):
        try:
            login_user = LoginUser.objects(Q(email=account) | Q(name=account), password=password).first()
            return login_user
        except Exception as e:
            print("query user error:{}".format(e))
            return None

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
