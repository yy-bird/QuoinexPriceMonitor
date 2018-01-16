import sched, time
from quoinex import Quoinex
from account import Account
from strategy import Strategy
from product import Product

s = sched.scheduler(time.time, time.sleep)
client = Quoinex(Account())
strategy = Strategy()

def scheduler(s, products):
    s.enter(2, 1, strategy.run, argument=(products,))
    s.run()

usd_balance = client.get_fiat_account_balance('USD')
sgd_balance = client.get_fiat_account_balance('SGD')
qash_balance = client.get_crypto_account_balance('QASH')
btc_balance = client.get_crypto_account_balance('BTC')
eth_balance = client.get_crypto_account_balance('ETH')

while 1:
    print('USD: {0} SGD: {1} QASH: {2} BTC: {3} ETH: {4}'.format(usd_balance, sgd_balance, qash_balance, btc_balance, eth_balance))
    products = [{"from_product": Product.QASHUSD, "mid_product": Product.QASHBTC, "to_product": Product.BTCUSD, "base_fund": 30},
                {"from_product": Product.QASHUSD, "mid_product": Product.QASHETH, "to_product": Product.ETHUSD, "base_fund": 20}]
    scheduler(s, products)