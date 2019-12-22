import os
import requests
from datetime import datetime
from .constants import USER, PASS
import functools


def get_token():
    jtd = datetime.now()
    JET_TOKEN_EXP_DATE = os.environ.get('JET_TOKEN_EXP_DATE')

    if JET_TOKEN_EXP_DATE:
        jtd = datetime.strptime(JET_TOKEN_EXP_DATE, '%Y-%m-%dT%H:%M:%SZ')

    if datetime.now() > jtd:
        data = {'user': USER, 'pass': PASS}

        response = requests.post('https://merchant-api.jet.com/api/token', json=data)

        if response:
            json_response = response.json()
            os.environ['JET_TOKEN'] = json_response['id_token']
            os.environ['JET_TOKEN_EXP_DATE'] = json_response['expires_on']
            return True
        else:
            return False
    return True


def refresh_token(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        get_token()
        response = func(*args, **kwargs)
        return response
    return wrapper_decorator