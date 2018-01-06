import sched, time
import requests
import json
import datetime
import jwt
from quoinex import Quoinex

s = sched.scheduler(time.time, time.sleep)
apiBase = 'https://api.quoine.com'

def check_price(productId, lowerLimit):
    r = requests.get(apiBase + '/products/' + productId)
    data = json.loads(r.text)
    info = {}
    info['text'] = '{0} - {1} buy: {2}, sell: {3}'.format(datetime.datetime.now().strftime("%I:%M%p"), data['currency_pair_code'], data['market_bid'], data['market_ask'])
    print(info)
    
    if data['market_ask'] <= lowerLimit:
        requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})


def scheduler(s):
    s.enter(5, 1, check_price, argument=('57', 1.03,))
    s.run()

client = Quoinex(183868, "Y7COWy8gDJmoKAFG7mIn/77pFXPyFXr1u5+Mg/P0me36b/cm4LVKa2LlZcMoqSLMSku6kUZGQWu7OHlQTBOXug==")
available_fiat_balance = client.get_fiat_account_balance('USD')
available_crypto_balance = client.get_crypto_account_balance('QASH')
init_fiat_balance = 35
target_crypto_balnace = 22 
