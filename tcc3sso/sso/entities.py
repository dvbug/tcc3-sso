# coding:utf-8
"""
    tcc3sso.sso.entities
    ~~~~~~~~~~~~~~~~~~~~

    sso entities module.
    :copyright: (c) 2015 by Vito.
    :license: GNU, see LICENSE for more details.
"""
import datetime
from ..core import db, Q
from mongoengine import NULLIFY

# class LoginUser(db.Document):
#     # 指定 mongo collection的名字
#     meta = {'collection': 'user'}
#
#     name = db.StringField(required=True, max_length=64)
#     password = db.StringField(required=True, max_length=256)
#     email = db.StringField(required=True, max_length=64)
#     description = db.StringField(max_length=240)
#
#     def __str__(self):
#         return "name:{}".format(self.name)
#
#     @classmethod
#     def register_user(cls, nick_name, password, email, description=None):
#         try:
#             login_user = LoginUser(name=nick_name, password=password, email=email, description=description)
#             login_user.save()
#             return True
#         except Exception as e:
#             print("register user error:{}".format(e))
#             return False
#
#     @classmethod
#     def query_user(cls, account, password):
#         try:
#             login_user = LoginUser.objects(Q(email=account) | Q(name=account), password=password).first()
#             return login_user
#         except Exception as e:
#             print("query user error:{}".format(e))
#             return None
#
#     @property
#     def is_active(self):
#         return True
#
#     @property
#     def is_authenticated(self):
#         return True
#
#     @property
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return self.id


GENDER_LIST = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unknown')
]


class UserPhone(db.Document):
    meta = {'collection': 'user_phone'}
    phone = db.StringField(required=True, max_length=11)


class UserProfile(db.Document):
    """User profile information."""
    meta = {'collection': 'user_profile'}

    nick_name = db.StringField(required=True, max_length=24)
    email = db.EmailField(required=True)

    real_name = db.StringField(max_length=24)
    # phones = db.ListField(db.ReferenceField(UserPhone, reverse_delete_rule=NULLIFY))
    birth = db.DateTimeField(default=datetime.datetime.now())
    gender = db.StringField(max_length=3, choices=GENDER_LIST, default=GENDER_LIST[2])
    brief_description = db.StringField(max_length=140)

    # is_active = db.BooleanField(required=True, default=True)
    # is_authenticated = db.BooleanField(required=True, default=True)

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


class LocalAuth(db.Document):
    meta = {'collection': 'local_auth'}

    user = db.ReferenceField(UserProfile, reverse_delete_rule=NULLIFY)
    password = db.StringField(required=True, max_length=64, min_length=4)

    @classmethod
    def try_login(cls, account, password):
        try:
            users = UserProfile.objects(Q(nick_name=account) | Q(email=account))
            login_auth = LocalAuth.objects(Q(user__in=users), password=password).first()
            if login_auth is not None:
                return login_auth.user
            else:
                return None
        except Exception as e:
            print('LocalAuth.try_login ERROR:{}'.format(e))
            return None

    @classmethod
    def try_register(cls, nick_name,
                     email,
                     password,
                     **kwargs):
        try:

            if nick_name in kwargs.keys():
                kwargs.pop(nick_name)
            if email in kwargs.keys():
                kwargs.pop(email)
            if password in kwargs.keys():
                kwargs.pop(password)

            user = UserProfile(nick_name=nick_name, email=email, **kwargs)
            user.save()
            local_auth = LocalAuth(password=password, user=user)
            local_auth.save()

            return local_auth
        except Exception as e:
            print('LocalAuth.try_register ERROR:{}'.format(e))
            return None
