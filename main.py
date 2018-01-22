import sched, time, requests
from quoinex import Quoinex
from account import Account
from strategy import Strategy
from product import Product

s = sched.scheduler(time.time, time.sleep)
client = Quoinex(Account())
strategy = Strategy()
trade_info = {}
has_exception = False

def scheduler_trade(s):
    product_trade = []
    product_trade.append({"from_product": Product.QASHUSD, "mid_product": Product.QASHBTC, "to_product": Product.BTCUSD, "base_fund": 15})
    product_trade.append({"from_product": Product.QASHUSD, "mid_product": Product.QASHETH, "to_product": Product.ETHUSD, "base_fund": 15})
    # product_trade.append({"from_product": Product.ETHUSD, "mid_product": Product.ETHBTC, "to_product": Product.BTCUSD, "base_fund": 15})
    # product_trade.append({"from_product": Product.QASHJPY, "mid_product": Product.QASHETH, "to_product": Product.ETHJPY, "base_fund": 1500})
    # product_trade.append({"from_product": Product.QASHJPY, "mid_product": Product.QASHBTC, "to_product": Product.BTCJPY, "base_fund": 1500})
    # product_trade.append({"from_product": Product.ETHJPY, "mid_product": Product.ETHBTC, "to_product": Product.BTCJPY, "base_fund": 3000})
    s.enter(2, 1, strategy.run, argument=(product_trade, trade_info, ))
    s.run()

while 1:
    try:
        scheduler_trade(s)
        if has_exception:
            has_exception = False
            requests.post("https://hooks.slack.com/services/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", data={"payload": {"text":"Recovered"}})
    except:
        print("exception")
        requests.post("https://hooks.slack.com/services/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", data={"payload": {"text":"Got excption"}})
        has_exception = True