# -*- coding: utf-8 -*-

from keys import *
from binance.client import Client
from binance.websockets import BinanceSocketManager
from datetime import datetime as dt


client = Client(API_KEY, API_SECRET)
market = 'BTCUSDT'.lower()
intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
stream_names = ["{}@kline_{}".format(market, i) for i in intervals]

def process_message(msg):
    data = msg['data']
    k = data['k']
    symbol, interval = k['s'], k['i']
    time_from, time_to = dt.fromtimestamp(int(k['t'])/1000), dt.fromtimestamp(int(k['T'])/1000)
    time_event = dt.fromtimestamp(int(data['E'])/1000)
    open_price, close_price, high_price, low_price = k['o'], k['c'], k['h'], k['l']
    volume, closed = k['v'], k['x']

    print("[{}]({}): ({} - {}) {} o: {}, c: {}, h: {}, l: {}, v: {}, closed: {}".format(
        symbol, interval, time_from, time_to, time_event,
        open_price, close_price, high_price, low_price,
        volume, closed))


bm = BinanceSocketManager(client)
conn_key = bm.start_multiplex_socket(stream_names, process_message)
bm.start()
