import sched, time
import requests, json
import datetime, jwt
from quoinex import Quoinex
from account import Account
from strategy1 import Strategy1

s = sched.scheduler(time.time, time.sleep)
client = Quoinex(Account())
strategy = Strategy1()

# def scheduler(s):
#     s.enter(5, 1, client.check_price, argument=('57',))
#     s.run()

def scheduler1(s):
    s.enter(6, 1, strategy.run)
    s.run()

available_fiat_balance = client.get_fiat_account_balance('USD')
available_crypto_balance = client.get_crypto_account_balance('QASH')

# print(client.buy(57, 1))

while 1:
    print('USD: {0} QASH: {1}'.format(available_fiat_balance, available_crypto_balance))
    scheduler1(s)