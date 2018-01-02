import sched, time
import requests
import json
import datetime

s = sched.scheduler(time.time, time.sleep)
apiBase = 'https://api.quoine.com/'

def check_price(productId, lowerLimit):
    r = requests.get(apiBase + '/products/' + productId)
    data = json.loads(r.text)
    info = {}
    info['text'] = '{0} - {1} buy: {2}, sell: {3}'.format(datetime.datetime.now().strftime("%I:%M%p"), data['currency_pair_code'], data['market_bid'], data['market_ask'])
    print(info)
    
    if data['market_bid'] >= lowerLimit:
        requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    

def scheduler(s):
   s.enter(5, 1, check_price, argument=('57', 0.9,))
   s.enter(5, 1, check_price, argument=('1', 15000,))
   s.run()

while(1):
    scheduler(s)