# coding:utf-8
"""
    tcc3sso.sso.token
    ~~~~~~~~~~~~~~~~~~~~

    sso token module.
"""
import uuid
import time
import threading

lock = threading.Lock()


class SSOToken(object):
    SSOTokenList = []

    def __init__(self, user_name=None):
        if user_name is not None:
            if type(user_name) == str:
                self.user_name = user_name
                self.__tickets = []
            else:
                raise TypeError()
        self.id = uuid.uuid1().hex
        self.__auth_time = time.time()
        self.time_out = 60*10

    def get_local_auth_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.__auth_time))

    def __is_timeout(self):
        # True: timeout
        # False: not timeout
        return (self.__auth_time + self.time_out) < time.time()

    def set_user(self, user_id):
        if type(user_id) == str:
            self.user_name = user_id
        else:
            raise TypeError()

    def set_login_id(self, login_id):
        pass

    def add_new_ticket(self):
        new_ticket = uuid.uuid1().hex
        if lock.acquire():
            self.__tickets.append(new_ticket)
            lock.release()
        return new_ticket

    def find_ticket(self, ticket):
        try:
            idx = self.__tickets.index(ticket)
            if idx >= 0:
                return True
            else:
                return False
        except Exception:
            return False

    def replace_ticket(self, old_ticket):
        try:
            new_ticket = None
            idx = self.__tickets.index(old_ticket)
            if lock.acquire():
                del self.__tickets[idx]
                new_ticket = uuid.uuid1().hex
                self.__tickets.append(new_ticket)
                lock.release()
            return new_ticket
        except Exception:
            return None

    @classmethod
    def find(cls, token_id):
        for item in SSOToken.SSOTokenList:
            if item.id == token_id:
                return item
        return None

    @classmethod
    def find_by_user_name(cls, user_name):
        for item in SSOToken.SSOTokenList:
            if item.user_name == user_name:
                return item
        return None

    @classmethod
    def __validate_token(cls, token):
        if token is None:
            raise ValueError('Null reference for token.')
        if not isinstance(token, SSOToken):
            raise TypeError('Incorrect type for token.')
        if not token.__is_timeout():
            return token
        else:
            try:
                if lock.acquire():
                    SSOToken.SSOTokenList.remove(token)
                    lock.release()
            except ValueError:
                pass
            finally:
                return False

    @classmethod
    def add_token(cls, token):
        if token is None:
            raise ValueError('Null reference for token.')
        if not isinstance(token, SSOToken):
            raise TypeError('Incorrect type for token.')
        
        try:
            if lock.acquire():
                SSOToken.SSOTokenList.append(token)
                lock.release()
        except ValueError as e:
            print('add_token error:{}'.format(e))

    @classmethod
    def remove_token(cls, token):
        if token is not None and isinstance(token, SSOToken):
            token_found = SSOToken.find(token.id)
            if token_found:
                idx = SSOToken.SSOTokenList.index(token_found)
                del SSOToken.SSOTokenList[idx]
                return True
        return False

    @classmethod
    def validate_token_id(cls, token_id):
        if not isinstance(token_id, str):
            raise TypeError('Incorrect type for token id')

        token = SSOToken.find(token_id)
        if token:
            if SSOToken.__validate_token(token):
                return token
        return False

    @classmethod
    def validate_ticket(cls, ticket):
        for item in SSOToken.SSOTokenList:
            if item.find_ticket(ticket):
                if SSOToken.__validate_token(item):
                    target_token = item
                    new_ticket = item.replace_ticket(ticket)
                    if new_ticket is not None:
                        return target_token, new_ticket
        return None


if __name__ == '__main__':
    token = SSOToken('vito2008')
    SSOToken.add_token(token)

    token_id = token.id
    ret = SSOToken.validate_token_id(token_id)

    if ret is False:
        print(type(ret))
        print('ret = {}'.format(str(ret)))
    else:
        print(type(ret))

    ticket = token.add_new_ticket()
    print('new ticket:{}'.format(ticket))
    result = SSOToken.validate_ticket(ticket)

    print(result[0].user_name)
    print(result[1])
