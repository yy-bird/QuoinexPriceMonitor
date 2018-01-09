#!/usr/bin/python

import sqlite3
import requests, datetime as dt

products = {
	'BTCUSD': 1,
	'ETHUSD': 27
}

"""
types:
product_data
trade_book
"""

def grab_product_data(product_id):
	resp = requests.get('https://api.quoine.com/products/{}/'.format(product_id))
	return resp.text


def grab_order_book(product_id):
	resp = requests.get('https://api.quoine.com/products/{}/price_levels'.format(product_id))
	return resp.text

if __name__ == '__main__':
	conn = sqlite3.connect('sqlite.db')
	c = conn.cursor()

	# Create table
	# c.execute('''CREATE TABLE btc (datetime text, type text, jsondata text)''')
	# c.execute('''CREATE TABLE eth (datetime text, type text, jsondata text)''')
	now = dt.datetime.now().__str__()

	# Insert a row of data
	c.execute("INSERT INTO btc VALUES ('{}','{}','{}')".format(now, 'product_data', grab_product_data(products['BTCUSD'])))
	c.execute("INSERT INTO btc VALUES ('{}','{}','{}')".format(now, 'trade_book', grab_order_book(products['BTCUSD'])))

	c.execute("INSERT INTO eth VALUES ('{}','{}','{}')".format(now, 'product_data', grab_product_data(products['ETHUSD'])))
	c.execute("INSERT INTO eth VALUES ('{}','{}','{}')".format(now, 'trade_book', grab_order_book(products['ETHUSD'])))

	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()