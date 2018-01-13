import sched, time
import requests, json
import datetime, jwt
from quoinex import Quoinex
from account import Account

s = sched.scheduler(time.time, time.sleep)
client = Quoinex(Account())

def scheduler(s):
    s.enter(5, 1, client.check_price, argument=('57',))
    s.run()

available_fiat_balance = client.get_fiat_account_balance('USD')
available_crypto_balance = client.get_crypto_account_balance('QASH')

while 1:
    print('USD: {0} QASH: {1}'.format(available_fiat_balance, available_crypto_balance))
    scheduler(s)