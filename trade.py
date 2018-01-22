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

    def _find_dutch_book(self):
        paths = self._find_possible_paths()
        results = []
        for p in paths:
            product = 1.0
            for i in range(len(p)-1):
                product = product * self.tm[p[i],p[i+1]]
            if product > 1:
                results.append(p)
        return results

    def _find_possible_paths(self):
        return [
            [0,1,0],
            [0,2,0],
            [0,1,2,0],
            [0,2,1,0],
        ]


if __name__ == '__main__':
    # initialize
    test_initialization()


