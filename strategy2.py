from quoinex import Quoinex
from account import Account
from product import Product
import json, requests, math

class Strategy2:
    client = Quoinex(Account())
    products_info = {}
    base_fund = 200

    def run(self, from_product, mid_product, to_product):
        self._get_products_info()
        self._positive_trade(from_product, mid_product, to_product)
        self._negative_trade(from_product, mid_product, to_product)

    def _positive_trade(self, from_product, mid_product, to_product):
        from_product_ask = self.products_info[from_product.value]["ask"]
        mid_product_bid = self.products_info[mid_product.value]["bid"]
        to_product_bid = self.products_info[to_product.value]["bid"]
        print('from_ask: {0}, mid_bid: {1}, to_bid: {2}'.format(from_product_ask, mid_product_bid, to_product_bid))
        print('positive: {0}'.format(100/from_product_ask*mid_product_bid*to_product_bid))

        # if 100/from_product_ask*mid_product_bid*to_product_bid > 100.2:
        #     amount = math.floor(self.base_fund/from_product_ask)
        #     real_amount1 = self.client.buy(from_product, amount)["quantity"]
        #     mid_resp = self.client.sell(mid_product, amount)
        #     price = float(mid_resp["price"])
        #     real_amount2 = mid_resp["quantity"]
        #     last_resp = self.client.sell(to_product, price*amount)
        #     sell_total = float(last_resp["price"]) * float(last_resp["quantity"])
        #     print('positive: calc_amount: {0}, real_buy_amount: {1}, real_sell_amount: {2}, earning: {3}'.format(amount, real_amount1, real_amount2, sell_total-self.base_fund))
        #     info = {'text': 'positive earning: {0}'.format(sell_total-self.base_fund)}
        #     requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    def _negative_trade(self, from_product, mid_product, to_product):
        from_product_bid = self.products_info[from_product.value]["bid"]
        mid_product_ask = self.products_info[mid_product.value]["ask"]
        to_product_ask = self.products_info[to_product.value]["ask"]
        print('negative: {0}'.format(100/to_product_ask/mid_product_ask*from_product_bid))

        # if 100/to_product_ask/mid_product_ask*from_product_bid > 100.2:
        #     amount = math.floor(100/to_product_ask * 100000000)/100000000
        #     real_amount1 = self.client.buy(to_product, amount)["quantity"]
        #     mid_buy_amount = math.floor(amount/mid_product_ask * 100000000)/100000000
        #     mid_resp = self.client.buy(mid_product, mid_buy_amount)
        #     real_amount2 = mid_resp["quantity"]
        #     last_resp = self.client.sell(from_product, mid_buy_amount)
        #     real_amount3 = last_resp["quantity"]
        #     sell_total = float(last_resp["price"]) * float(last_resp["quantity"])
        #     print('negative: calc_amount: {0}, real_amount1: {1}, mid_buy_amount: {2}, real_mid_buy_amount: {3}, real_amount3: {4}, earning: {5}'.format(amount, real_amount1, mid_buy_amount, real_amount2, real_amount3, sell_total-100))
        #     info = {'text': 'negative earning: {0}'.format(sell_total-100)}
        #     requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

    def _get_products_info(self):
        products_info = self.client.get_products_info()
        for x in products_info:
            self.products_info[int(x["id"])] = {'ask': float(x['market_ask']), 'bid': float(x['market_bid'])}