from quoinex import Quoinex
from account import Account
from product import Product
import json, requests, math

class Strategy3:
    client = Quoinex(Account())
    products_info = {}
    base_fund = 150

    def run(self, patterns):
        self._get_products_info()
        for pattern in patterns:
            self._positive_trade(pattern["from_product"], pattern["mid_product"], pattern["to_product"])
            self._negative_trade(pattern["from_product"], pattern["mid_product"], pattern["to_product"])

    def _positive_trade(self, from_product, mid_product, to_product):
        from_product_ask = self.products_info[from_product.value]["ask"]
        mid_product_bid = self.products_info[mid_product.value]["bid"]
        to_product_bid = self.products_info[to_product.value]["bid"]
        print('{0} positive: {1}'.format(mid_product.name, 100/from_product_ask*mid_product_bid*to_product_bid))

        if 100/from_product_ask*mid_product_bid*to_product_bid > 100.2:
            amount = math.floor(self.base_fund/from_product_ask)
            buy_resp = self.client.buy(from_product, amount)
            real_amount1 = float(buy_resp["quantity"])
            buy_price = float(buy_resp["price"])
            mid_resp = self.client.sell(mid_product, amount)
            price = float(mid_resp["price"])
            real_amount2 = mid_resp["quantity"]
            last_resp = self.client.sell(to_product, price*amount)
            sell_total = float(last_resp["price"]) * float(last_resp["quantity"])
            print('{0} positive: calc_amount: {1}, real_buy_amount: {2}, real_sell_amount: {3}, earning: {4}'.format(mid_product.name, amount, real_amount1, real_amount2, sell_total-real_amount1*buy_price))
            info = {'text': '{0} positive earning: {1}'.format(mid_product.name, sell_total-real_amount1*buy_price}
            requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    def _negative_trade(self, from_product, mid_product, to_product):
        from_product_bid = self.products_info[from_product.value]["bid"]
        mid_product_ask = self.products_info[mid_product.value]["ask"]
        to_product_ask = self.products_info[to_product.value]["ask"]
        print('{0} negative: {1}'.format(mid_product.name, 100/to_product_ask/mid_product_ask*from_product_bid))

        if 100/to_product_ask/mid_product_ask*from_product_bid > 100.2:
            amount = math.floor(self.base_fund/to_product_ask * 100000000)/100000000
            buy_resp = self.client.buy(to_product, amount)
            real_amount1 = float(buy_resp["quantity"])
            real_price = float(buy_resp["price"])
            mid_buy_amount = math.floor(real_amount1/mid_product_ask * 100000000)/100000000
            mid_resp = self.client.buy(mid_product, mid_buy_amount)
            real_mid_buy_amount = mid_resp["quantity"]
            last_resp = self.client.sell(from_product, mid_buy_amount)
            print(json.dumps(last_resp))
            real_sell_amount = last_resp["quantity"]
            sell_total = float(last_resp["price"]) * float(last_resp["quantity"])
            print('{0} negative: calc_amount: {1}, real_amount1: {2}, mid_buy_amount: {3}, real_mid_buy_amount: {4}, real_amount3: {5}, earning: {6}'.format(mid_product, amount, real_amount1, mid_buy_amount, real_mid_buy_amount, real_sell_amount, sell_total-real_amount1*real_price))
            info = {'text': '{0} negative earning: {1}'.format(mid_product.name, sell_total-real_amount1*real_price)}
            requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    def _get_products_info(self):
        products_info = self.client.get_products_info()
        for x in products_info:
            self.products_info[int(x["id"])] = {'ask': float(x['market_ask']), 'bid': float(x['market_bid'])}