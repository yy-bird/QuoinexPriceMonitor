from quoinex import Quoinex
from account import Account
import json, requests

class Strategy1:
    client = Quoinex(Account())
    trade_quantity = 1

    def run(self):
        QASHUSD_sell_price_level = float(self.client.get_orderbook('57')['sell_price_levels'][0][0]) #QASHUSD
        QASHBTC_buy_price_level = float(self.client.get_orderbook('52')['buy_price_levels'][0][0])   #QASHBTC
        BTCUSD_buy_price_level = float(self.client.get_orderbook('1')['buy_price_levels'][0][0])     #BTCUSD

        print(100/QASHUSD_sell_price_level*QASHBTC_buy_price_level*BTCUSD_buy_price_level)

        if 100/QASHUSD_sell_price_level*QASHBTC_buy_price_level*BTCUSD_buy_price_level > 100:
             qash_quantity = float(self.client.buy(57, self.trade_quantity)["quantity"])
             btc_quantity = float(self.client.sell(52, qash_quantity)["quantity"])
             usd_amount = float(self.client.sell(1, btc_quantity)["price"]) * btc_quantity
             info = {'text': "buy use {0} usd, sell for {1}, earn {2}".format(qash_quantity*self.trade_quantity, usd_amount, usd_amount-qash_quantity*100)}
             print(info)
             requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})

        QASHUSD_buy_price_level = float(self.client.get_orderbook('57')['buy_price_levels'][0][0]) #QASHUSD
        QASHBTC_sell_price_level = float(self.client.get_orderbook('52')['sell_price_levels'][0][0])   #QASHBTC
        BTCUSD_sell_price_level = float(self.client.get_orderbook('1')['sell_price_levels'][0][0])     #BTCUSD

        print(100/BTCUSD_sell_price_level/QASHBTC_sell_price_level*QASHUSD_buy_price_level)

        if 100/BTCUSD_sell_price_level/QASHBTC_sell_price_level*QASHUSD_buy_price_level > 100:
            btc_quantity = float(self.client.buy(1, 100/BTCUSD_sell_price_level)["quantity"])
            qash_quantity = float(self.client.buy(52, btc_quantity/QASHBTC_sell_price_level)["quantity"])
            usd_amount = float(self.client.sell(57, qash_quantity)["price"]) * qash_quantity
             
            info = {'text': "buy use {0} usd, sell for {1}, earn {2}".format(100, usd_amount, usd_amount-100)}
            print(info)
            requests.post("https://hooks.slack.com/services/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", data={"payload": json.dumps(info)})