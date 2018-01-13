from quoinex import Quoinex
from account import Account

class Strategy:
    client = Quoinex(Account())
    available_fiat_balance = client.get_fiat_account_balance('USD')
    available_crypto_balance = client.get_crypto_account_balance('QASH')
    min_reserve_fiat=200
    min_reserve_crypto=100
    trade_step=10

    def __init__(self, productId):
        self.productId = productId

    def trade(self):
        price = self.client.get_price(self.productId)
        buy_price = price['market_bid']
        sell_price = price['market_ask']

        # if(self.available_fiat_balance > self.min_reserve_fiat and self.available_crypto_balance < self.min_reserve_crypto){
        #     self.client.limit
        # }