import requests, jwt
import time

HOST = 'https://api.quoine.com'
headers = {'X-Quoine-API-Version': '2'}


def get_nonce():
    return int(time.time() * 1000)


PRODUCT_ID = {
    'BTCUSD': 1,
    'BTCJPY': 5,
    'BTCSGD': 7,
    'ETHUSD': 27,
    'ETHJPY': 29,
    'ETHBTC': 37,
    'QASHJPY': 50,
    'QASHETH': 51,
    'QASHBTC': 52,
    'QASHUSD': 57,
}


class QuoinexAPI(object):
    def __init__(self):
        pass

    def load_profile(self, API_Token_ID, API_Secret):
        self.token_id = API_Token_ID
        self.secret = API_Secret

    def _request(self, path, is_public_api=False):
        if not is_public_api:
            auth_payload = {
                'path': path,
                'nonce': get_nonce(),
                'token_id': self.token_id
            }
            signature = jwt.encode(auth_payload, self.secret, algorithm='HS256')
            headers['X-Quoine-Auth'] = signature

        headers['Content-Type'] = 'application/json'
        return requests.get(HOST + path, headers=headers)

    #### Public API ####
    def get_products(self):
        path = '/products'
        resp = self._request(path, is_public_api=True)
        print resp.text

    def get_product_by_id(self, product_id):
        path = '/products/{}'.format(product_id)
        resp = self._request(path, is_public_api=True)
        print resp.text

    def get_order_book_by_id(self, product_id):
        path = '/products/{}/price_levels/'.format(product_id)
        resp = self._request(path, is_public_api=True)
        print resp.text

    def get_execution_by_id(self, product_id):
        path = '/executions?product_id={}&limit=2&page=1'.format(product_id)
        resp = self._request(path, is_public_api=True)
        print resp.text

    def get_execution_by_id_timestamp(self, product_id, timestamp):
        path = '/executions?product_id={}&timestamp={}&limit=20'.format(product_id, timestamp)
        resp = self._request(path, is_public_api=True)
        print resp.text

    #### Authenticated API ####
    def get_product_order(self, product_id):
        path = '/orders?product_id={}'.format(product_id)
        resp = self._request(path, is_public_api=False)
        print resp.text


if __name__ == '__main__':
    # API_Token_ID='285781'
    # API_Secret='zQvtYh5BKoAnRhaEX3Z9Ieo+tzvDSk5rg4uduWu0QpHpHihbsgZzYZz6EL/HTAAoGpV0IhNXq6zQoM7UR7mF4g=='
    API_Token_ID = '285801'
    API_Secret = 'RwnvHBy7fR/pEEXnfERTh75ALRBhx5eRVcomI8a1aHPau3m/yyY7Ps0xaegVT0yeUul2ETzPP3IbQpO0xu4m7A=='
    api = QuoinexAPI()
    api.load_profile(API_Token_ID, API_Secret)
    api.get_product_order()
