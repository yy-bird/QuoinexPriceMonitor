import sched, time
from quoinex import Quoinex
from account import Account
from strategy1 import Strategy1
from strategy2 import Strategy2
from strategy3 import Strategy3
from product import Product

s = sched.scheduler(time.time, time.sleep)
client = Quoinex(Account())
# strategy = Strategy1()
# strategy = Strategy2()
strategy = Strategy3()

def scheduler1(s, products):
    s.enter(2, 1, strategy.run, argument=(products,))
    s.run()

available_fiat_balance = client.get_fiat_account_balance('USD')
available_crypto_balance = client.get_crypto_account_balance('QASH')

while 1:
    print('USD: {0} QASH: {1}'.format(available_fiat_balance, available_crypto_balance))
    products = [{"from_product": Product.QASHUSD, "mid_product": Product.QASHBTC, "to_product": Product.BTCUSD}]#,
                #{"from_product": Product.QASHUSD, "mid_product": Product.QASHETH, "to_product": Product.ETHUSD}]
    scheduler1(s, products)