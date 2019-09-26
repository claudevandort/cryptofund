# -*- coding: utf-8 -*-

from keys import *
from binance.client import Client
from binance.websockets import BinanceSocketManager

client = Client(API_KEY, API_SECRET)
market = 'BTCUSDT'

def process_message(msg):
    k = msg['k']
    print("[{}]: ({} - {}) {} o: {}, c: {}, h: {}, l: {}, v: {}".format(k['s'], k['t'], k['T'], msg['E'], k['o'], k['c'], k['h'], k['l'], k['v']))


bm = BinanceSocketManager(client)
conn_key = bm.start_kline_socket(market, process_message)
bm.start()
