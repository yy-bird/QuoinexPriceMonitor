import sched, time
from quoinex import Quoinex
from account import Account
from strategy import Strategy
from product import Product


s = sched.scheduler(time.time, time.sleep)
client = Quoinex(Account())
strategy = Strategy()
trade_info = {"counter": 0}

def scheduler_trade(s):
    product_trade = [{"from_product": Product.QASHUSD, "mid_product": Product.QASHBTC, "to_product": Product.BTCUSD, "base_fund": 50, "has_negative": True}]
    s.enter(2, 1, strategy.run, argument=(product_trade, trade_info, ))
    s.run()

usd_balance = client.get_fiat_account_balance('USD')
sgd_balance = client.get_fiat_account_balance('SGD')
qash_balance = client.get_crypto_account_balance('QASH')
btc_balance = client.get_crypto_account_balance('BTC')
eth_balance = client.get_crypto_account_balance('ETH')

while 1:
    print('USD: {0} SGD: {1} QASH: {2} BTC: {3} ETH: {4}'.format(usd_balance, sgd_balance, qash_balance, btc_balance, eth_balance))
    scheduler_trade(s)