import random
import re


class AuthCookieFactory():
    @staticmethod
    def generate():
        import string
        sys_random = random.SystemRandom()
        alphabet = string.ascii_letters + string.digits
        while True:
            password = ''.join(sys_random.choice(alphabet) for i in range(10))
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
                break
        return Cookie(password)

    @staticmethod
    def get_from_headers(headers):
        cookie = str(headers['http-cookie']) if 'http-cookie' in headers else ''
        token_re = re.compile('nazwa=(.*)')
        x = token_re.findall(cookie)
        if x is None:
            raise Exception("No token Found")
        return Cookie(str(x[0]))


class Cookie():
    def __init__(self, token):
        self.token = token

    def get_token(self):
        return (self.token)

    def return_cookie(self):
        return (
        'nazwa={0}; expires=Fri, 07-Jun-2019 19:40:00 GMT; Max-Age=63071999; path=/; domain=.rozanovk.tk; '.format(
            self.token))
