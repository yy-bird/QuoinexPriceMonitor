from quoinex import Quoinex
from account import Account
from product import Product
import json, requests, math

class Strategy:
    client = Quoinex(Account())
    products_info = {}

    def run(self, patterns):
        self._get_products_info()
        for pattern in patterns:
            self._positive_trade(pattern)
            self._negative_trade(pattern)

    def _positive_trade(self, pattern):
        from_product_ask = self.products_info[pattern["from_product"].value]["ask"]
        mid_product_bid = self.products_info[pattern["mid_product"].value]["bid"]
        to_product_bid = self.products_info[pattern["to_product"].value]["bid"]
        ratio = 100/from_product_ask*mid_product_bid*to_product_bid        
        print('{0} positive: {1}'.format(pattern["mid_product"].name, ratio))

        if ratio > 100.2:
            amount = math.floor(pattern["base_fund"]/from_product_ask)
            # if float(self.client.get_orderbook(pattern["from_product"])["sell_price_levels"][1]) > amount*0.75:
            from_buy = self.client.buy(pattern["from_product"], amount)
            mid_sell= self.client.sell(pattern["mid_product"], from_buy["quantity"])
            to_sell = self.client.sell(pattern["to_product"], mid_sell["total"])
            print('{0} positive: start: {1}, end: {2}, earning: {3}'.format(pattern["mid_product"].name, from_buy["total"], to_sell["total"], to_sell["total"]-from_buy["total"]))
            info = {'text': '{0} positive earning: {1}'.format(pattern["mid_product"].name, round(to_sell["total"]-from_buy["total"], 3))}
            requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    def _negative_trade(self, pattern):
        from_product_bid = self.products_info[pattern["from_product"].value]["bid"]
        mid_product_ask = self.products_info[pattern["mid_product"].value]["ask"]
        to_product_ask = self.products_info[pattern["to_product"].value]["ask"]
        ratio = 100/to_product_ask/mid_product_ask*from_product_bid
        print('{0} negative: {1}'.format(pattern["mid_product"].name, ratio))

        if ratio > 100.2:
            amount = self._process_price(pattern["base_fund"]/to_product_ask)
            to_buy = self.client.buy(pattern["to_product"], amount)
            mid_buy = self.client.buy(pattern["mid_product"], self._process_price(to_buy["quantity"]/mid_product_ask))
            from_sell = self.client.sell(pattern["from_product"], mid_buy["quantity"])
            print('{0} negative: start: {1}, end: {2}, earning: {3}'.format(pattern["mid_product"].name, to_buy["total"], to_buy["total"], from_sell["total"]-to_buy["total"]))
            info = {'text': '{0} negative earning: {1}'.format(pattern["mid_product"].name, round(from_sell["total"]-to_buy["total"], 3))}
            requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    def _get_products_info(self):
        products_info = self.client.get_products_info()
        for x in products_info:
            self.products_info[int(x["id"])] = {'ask': float(x['market_ask']), 'bid': float(x['market_bid'])}
    
    def _process_price(self, price):
        return math.floor(price * 100000000)/100000000