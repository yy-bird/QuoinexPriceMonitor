import requests, jwt
import time
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

    def get_products_info(self):
        resp = self._request('/products')
        return json.loads(resp)

    def get_orderbook(self, product):
        resp = self._request('/products/{0}/price_levels'.format(product.value))
        return json.loads(resp)

    def buy(self, product, quantity, order_type='market', price=0):
        order = self._create_order('buy', product.value, order_type, quantity, price)
        content = self._request("/orders/", method='post', data=order, is_private=True)
        resp = json.loads(content)
        return {"quantity": float(resp["quantity"]), "price": float(resp["price"]), "total": float(resp["quantity"]) * float(resp["price"])}

    def sell(self, product, quantity, order_type='market', price=0):
        order = self._create_order('sell', product.value, order_type, quantity, price)
        content = self._request("/orders/", method='post', data=order, is_private=True)
        resp = json.loads(content)
        return {"quantity": float(resp["quantity"]), "price": float(resp["price"]), "total": float(resp["quantity"]) * float(resp["price"])}

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
            return r.text
        elif method == 'post':
            r = requests.post(self.api_base + path, headers=headers, json=data)
            return r.text
        else:
            return 'Invalid Method'