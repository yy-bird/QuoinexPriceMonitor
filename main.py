import sched, time
import requests
import json
import datetime
import jwt

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

    
def buy_strategy():
    return

def sell_strategy():
    return

def get_token(path):
    encoded = jwt.encode(
        {'path':path,'nonce': int(round(time.time() * 1000)), 'token_id': 183868},
        "Y7COWy8gDJmoKAFG7mIn/77pFXPyFXr1u5+Mg/P0me36b/cm4LVKa2LlZcMoqSLMSku6kUZGQWu7OHlQTBOXug==", 
        algorithm='HS256')
    return encoded

def scheduler(s):
    s.enter(5, 1, check_price, argument=('57', 1.03,))
    s.run()

def get_fiat_account_balance(currency):
    path = '/fiat_accounts'
    r = requests.get(apiBase + path, headers = {'X-Quoine-API-Version':'2','X-Quoine-Auth':get_token(path)})
    fiat_list = json.loads(r.content)
    for x in fiat_list:
        if x['currency'] == currency:
            return x['balance']
        else:
            return None

#print(get_token('/fiat_accounts'))
#get_token('/accounts/balance')
print(get_fiat_account_balance('USD'))
#while(1):
    #scheduler(s)