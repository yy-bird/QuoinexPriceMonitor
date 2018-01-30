from quoinex import Quoinex
from account import Account
from product import Product
import json, requests, math, os

class Strategy:
    client = Quoinex(Account())
    products_info = {}
    trade_info = {}
    usd_balance = client.get_fiat_account_balance('USD')
    sgd_balance = client.get_fiat_account_balance('SGD')
    jpy_balance = client.get_fiat_account_balance('JPY')

    def run(self, patterns, trade_info):
        os.system("cls")
        os.system("clear")
        print('USD: {0} SGD: {1} JPY: {2}'.format(self.usd_balance, self.sgd_balance, self.jpy_balance))
        self._get_products_info()
        self.trade_info = trade_info
        for pattern in patterns:
            result = self._positive_trade(pattern)
            # result = result or self._negative_trade(pattern)
            if result:
                break
        self._print_trade_info()

    def _positive_trade(self, pattern):
        from_product_ask = self.products_info[pattern["from_product"].value]["ask"]
        mid_product_bid = self.products_info[pattern["mid_product"].value]["bid"]
        to_product_bid = self.products_info[pattern["to_product"].value]["bid"]
        ratio = 100/from_product_ask*mid_product_bid*to_product_bid

        print('-------------------------------------------------------------------')    
        key = '{0}-{1}-{2}-positive'.format(pattern["from_product"].name, pattern["mid_product"].name, pattern["to_product"].name)       
        print('{0}: {1}'.format(key, ratio))

        if ratio > 100.1:
            order_book_from = self.client.get_orderbook(pattern["from_product"])
            order_book_to = self.client.get_orderbook(pattern["mid_product"])
            amount = math.floor(pattern["base_fund"]/from_product_ask)
            if self.client.get_orderbook(pattern["from_product"])["ask"][1] < amount or self.client.get_orderbook(pattern["mid_product"])["bid"][1] < amount:
                print("from ask amount: {0}, to buy amount: {1}".format(order_book_from["ask"][1], amount))
                print("mid bid amount: {0}, to buy amount: {1}".format(order_book_to["bid"][1], amount))
                return False 

            from_buy = self.client.buy(pattern["from_product"], amount)
            mid_sell= self.client.sell(pattern["mid_product"], from_buy["quantity"])
            to_sell = self.client.sell(pattern["to_product"], mid_sell["total"])
            earning = to_sell["total"]-from_buy["total"]
            print('{0} positive: start: {1}, end: {2}, earning: {3}'.format(pattern["mid_product"].name, from_buy["total"], to_sell["total"], earning))
            info = {'text': '{0} positive earning: {1}'.format(pattern["mid_product"].name, round(earning, 3))}
            requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})
            if key not in self.trade_info:
                self.trade_info[key] = 0
            self.trade_info[key] += earning
            return True
        return False

    def _negative_trade(self, pattern):
        from_product_bid = self.products_info[pattern["from_product"].value]["bid"]
        mid_product_ask = self.products_info[pattern["mid_product"].value]["ask"]
        to_product_ask = self.products_info[pattern["to_product"].value]["ask"]
        ratio = 100/to_product_ask/mid_product_ask*from_product_bid
        key = '{0}-{1}-{2}-negative'.format(pattern["from_product"].name, pattern["mid_product"].name, pattern["to_product"].name)               
        print('{0}: {1}'.format(key, ratio))

        if ratio > 100.1:
            order_book = self.client.get_orderbook(pattern["from_product"])
            amount = self._process_price(pattern["base_fund"]/to_product_ask)    
            if order_book["bid"][1] < pattern["base_fund"]/order_book["bid"][0]:
                print("bid amount: {0}, to buy amount: {1}".format(order_book["bid"][1], pattern["base_fund"]/order_book["bid"][0]))
                return False  
            to_buy = self.client.buy(pattern["to_product"], amount)
            mid_buy = self.client.buy(pattern["mid_product"], self._process_price(to_buy["quantity"]/mid_product_ask))
            from_sell = self.client.sell(pattern["from_product"], mid_buy["quantity"])
            earning = from_sell["total"]-to_buy["total"]
            print('{0} negative: start: {1}, end: {2}, earning: {3}'.format(pattern["mid_product"].name, to_buy["total"], to_buy["total"], earning))
            info = {'text': '{0} negative earning: {1}'.format(pattern["mid_product"].name, round(earning, 3))}
            requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})
            if key not in self.trade_info:
                self.trade_info[key] = 0
            self.trade_info[key] += earning
            return True
        return False

    def _print_trade_info(self):
        print("************************************")
        for attr, value in self.trade_info.items():
            print("{0} earning {1}".format(attr, value))
        print("************************************")

    def _get_products_info(self):
        products_info = self.client.get_products_info()
        for x in products_info:
            if(x['market_ask'] == None or x['market_bid'] == None):
                continue
            self.products_info[int(x["id"])] = {'ask': float(x['market_ask']), 'bid': float(x['market_bid'])}
    
    def _process_price(self, price):
        return math.floor(price * 100000000)/100000000