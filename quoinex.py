import requests
import jwt
import time
import json

class Quoinex:
    api_base = 'https://api.quoine.com'

    def __init__(self, token_id, secret):
        self.token_id = token_id
        self.secret = secret
    
    def get_fiat_account_balance(self, currency):
        path = '/fiat_accounts'
        fiat_list = json.loads(self.request(path, is_private = True))
        for x in fiat_list:
            if x['currency'] == currency:
                return x['balance']
            else:
                return None

    def get_crypto_account_balance(self, currency):
        path = '/crypto_accounts'
        fiat_list = json.loads(self.request(path, is_private = True))
        for x in fiat_list:
            if x['currency'] == currency:
                return x['balance']
            else:
                return None

    def get_token(self, path):
        encoded = jwt.encode({'path':path,'nonce': int(round(time.time() * 1000)), 'token_id': self.token_id}, self.secret, algorithm='HS256')
        return encoded

    def request(self, path, method='get', data={}, is_private=False):
        headers = {'X-Quoine-API-Version':'2'}
        if(is_private):
            headers['X-Quoine-Auth'] = self.get_token(path)

        if method == 'get':
            r = requests.get(self.api_base + path, headers = headers)
            return r.content
        elif method == 'post':
            r = requests.post(self.api_base + path, headers = headers, data = data)
            return r.content
        else:
            return 'Invalid Method'