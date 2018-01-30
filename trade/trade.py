"""
if three are 3 nodes,

1. assign weights to edges.
2. starting from the base node, go through each node in sequence and finally run back to base node
3. calculate the product for weight. if >1, buy in the same direction as step 2, else buy in the opposite direction.
4. check that the quantity in order book are in abundance
5. make purchase

"""

import numpy as np
import random
class currency(object):

    def __init__(self, currency_code):
        self.code=currency_code

CURRENCY = ['USD', 'QASH', 'BTC']

def test_initialization():
    agent = TradeAgent()
    route = [0, 1, 2, 0]
    for i in range(len(route) - 1):
        agent.tm[route[i],route[i+1]] = random.random()


    route = [0, 2, 1, 0]
    for i in range(len(route) - 1):
        agent.tm[route[i],route[i+1]] = random.random()

    print 'expect a metric with diagonal value 0'
    print agent.tm


class TradeAgent(object):
    def __init__(self):
        self.currency_list = ['usd', 'btc', 'qash']
        num_currency = len(self.currency_list)
        self.tm = np.zeros(shape=(num_currency,num_currency))  # transition_matrix
        self.paths = self.get_possible_paths()  # get possible trading sequences

        # this is how transition matrix looks like
        # buy       USD     QASH    BTC
        # with
        # USD       1       0.3     0.9
        # QASH      3.2     1       1.3
        # BTC       13      7.1     1

    def trade(self):
        # 1. send request and update transition matrix
        self.update_price_matrix()
        # 2. get dutch book path(trading sequence)
        dutch_book_paths = self.find_dutch_book()
        # 3. place orders based on order book
        self.place_orders(dutch_book_paths)


    def find_dutch_book(self):
        # results = []
        # for p in self.paths:
        #     if self._is_path_dutch_book(p):
        #         results.append(p)
        # return results
        return [p for p in self.paths if self._is_path_dutch_book(p)]

    def _is_path_dutch_book(self, p):
        product = 1.0
        for i in range(len(p) - 1):
            product = product * self.tm[p[i], p[i + 1]]
        return product > 1

    def update_price_matrix(self):
        # there is not necessary enough abundant amount of bid/ask for the best price,
        # update the average price based on the order amount from trade book.
        # the average is take over the a minimum trade quantity
        pass

    def place_orders(self, paths):
        for p in paths:
            self._place_order(p)

    def _place_order(self, path):
        pass

    def get_possible_paths(self):
        # todo: currently, assume there are only 3 currency. the return is hardcoded.
        # this function should always return a fixed series of paths during run time,
        # as long as currency list is fixed
        return [
            [0,1,0],
            [0,2,0],
            [0,1,2,0],
            [0,2,1,0],
        ]


if __name__ == '__main__':
    import sched, time
    agent = TradeAgent()
    s = sched.scheduler(time.time, time.sleep)
    while 1:
        try:
            s.enter(2, 1, agent.trade)
            s.run()
            if has_exception:
                has_exception = False
                print 'Recovered'
                # requests.post("https://hooks.slack.com/services/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", data={"payload": {"text":"Recovered"}})
        except:
            print("exception")
            # requests.post("https://hooks.slack.com/services/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", data={"payload": {"text":"Got excption"}})
            has_exception = True
            print 'Error'
    #
    # last, clear orders if orders are not filled



