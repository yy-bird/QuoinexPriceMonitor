import requests
import jwt
import time, datetime
import json

class Quoinex:
    api_base = 'https://api.quoine.com'

    def __init__(self, account):
        self.token_id = account.token_id
        self.secret = account.secret
    
    def get_fiat_account_balance(self, currency):
        path = '/fiat_accounts'
        fiat_list = json.loads(self._request(path, is_private = True))
        for x in fiat_list:
            if x['currency'] == currency:
                return x['balance']
        return None

    def get_crypto_account_balance(self, currency):
        path = '/crypto_accounts'
        crypto_list = json.loads(self._request(path, is_private = True))
        for x in crypto_list:
            if x['currency'] == currency:
                return x['balance']
        return None

    def get_price(self, productId):
        resp = self._request('/products/' + productId)
        return json.loads(resp)

    def get_orderbook(self, productId):
        resp = self._request("/products/" + productId + "/price_levels")
        return json.loads(resp)

    def buy(self, product_id, quantity, order_type='market', price=0):
        order = self._create_order('buy', product_id, order_type, quantity, price)
        resp = self._request("/orders/", method='post', data=order, is_private=True)
        return json.loads(resp)

    def sell(self, product_id, quantity, order_type='market', price=0):
        order = self._create_order('sell', product_id, order_type, quantity, price)
        resp = self._request("/orders/", method='post', data=order, is_private=True)
        return json.loads(resp)

    def _create_order(self, side, product_id, order_type, quantity, price):
        order = {}
        order['order'] = {}
        order['order']['order_type'] = order_type
        order['order']['product_id'] = product_id
        order['order']['side'] = side
        order['order']['quantity'] = quantity
        order['order']['price'] = price
        return order

    def _get_token(self, path):
        encoded = jwt.encode({'path':path,'nonce': int(time.time() * 1000), 'token_id': self.token_id}, self.secret, algorithm='HS256')
        return encoded

    def _request(self, path, method='get', data={}, is_private=False):
        headers = {'X-Quoine-API-Version':'2'}
        if(is_private):
            headers['X-Quoine-Auth'] = self._get_token(path)

        if method == 'get':
            r = requests.get(self.api_base + path, headers = headers)
            return r.content
        elif method == 'post':
            r = requests.post(self.api_base + path, headers=headers, json=data)
            return r.content
        else:
            return 'Invalid Method'