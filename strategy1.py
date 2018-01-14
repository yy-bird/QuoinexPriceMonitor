from quoinex import Quoinex
from account import Account
import json, requests, math
from product import Product

class Strategy1:
    client = Quoinex(Account())
    trade_quantity = 10

    def run(self):
        QASHUSD_sell_price_level = float(self.client.get_orderbook(Product.QASHUSD)['sell_price_levels'][0][0]) #QASHUSD
        QASHBTC_buy_price_level = float(self.client.get_orderbook(Product.QASHBTC)['buy_price_levels'][0][0])   #QASHBTC
        BTCUSD_buy_price_level = float(self.client.get_orderbook(Product.BTCUSD)['buy_price_levels'][0][0])     #BTCUSD

        print(100/QASHUSD_sell_price_level*QASHBTC_buy_price_level*BTCUSD_buy_price_level)

        # if 100/QASHUSD_sell_price_level*QASHBTC_buy_price_level*BTCUSD_buy_price_level > 100.5:
        #      resp1 = self.client.buy(Product.QASHUSD, self.trade_quantity)
        #      qash_quantity = float(resp1["quantity"])
        #      btc_quantity = float(self.client.sell(Product.QASHBTC, self.trade_quantity)["quantity"])
        #      resp2 = self.client.sell(Product.BTCUSD, btc_quantity)
        #      print(resp2)
        #      usd_amount = float(resp2["price"]) * btc_quantity
        #      info = {'text': "buy use {0} usd, sell for {1}, earn {2}".format(qash_quantity*self.trade_quantity, usd_amount, usd_amount-qash_quantity*100)}
        #      print(info)
        #      requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

        QASHUSD_buy_price_level = float(self.client.get_orderbook(Product.QASHUSD)['buy_price_levels'][0][0]) #QASHUSD
        QASHBTC_sell_price_level = float(self.client.get_orderbook(Product.QASHBTC)['sell_price_levels'][0][0])   #QASHBTC
        BTCUSD_sell_price_level = float(self.client.get_orderbook(Product.BTCUSD)['sell_price_levels'][0][0])     #BTCUSD

        print(100/BTCUSD_sell_price_level/QASHBTC_sell_price_level*QASHUSD_buy_price_level)
        # print(str(QASHUSD_buy_price_level) + ":" + str(QASHBTC_sell_price_level) + ":" + str(BTCUSD_sell_price_level))

        # if 100/BTCUSD_sell_price_level/QASHBTC_sell_price_level*QASHUSD_buy_price_level > 100.5:
        #     usd = 100
        #     btc_quantity = float(self.client.buy(Product.BTCUSD, math.floor(usd/BTCUSD_sell_price_level*10000)/10000)["quantity"])
        #     qash_quantity = float(self.client.buy(Product.QASHBTC, math.floor(btc_quantity/QASHBTC_sell_price_level*10000)/10000)["quantity"])
        #     usd_amount = float(self.client.sell(Product.QASHUSD, qash_quantity)["price"]) * qash_quantity
             
        #     info = {'text': "buy use {0} usd, sell for {1}, earn {2}".format(usd, usd_amount, usd_amount-usd)}
        #     print(info)
        #     requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})