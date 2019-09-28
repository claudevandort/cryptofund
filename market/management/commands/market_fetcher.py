from django.core.management.base import BaseCommand, CommandError
from service import Service, find_syslog
import logging
from logging.handlers import SysLogHandler
import keys
from binance.client import Client
from binance.websockets import BinanceSocketManager
from datetime import datetime as dt
import pytz
from market.models import Exchange, Market, ExchangeMarket, Candle, Interval


class MarketFetcher:
    exchange, market = Exchange.objects.get(name='Binance'), Market.objects.get(name='BTCUSDT')
    exchange_market = ExchangeMarket.objects.get(exchange=exchange, market=market)
    command = None

    def __init__(self, *args, **kwargs):
        self.command = kwargs['command']

    def log(self, msg):
        self.command.stdout.write(self.command.style.SUCCESS(msg))

    def start(self):
        client = Client(keys.API_KEY, keys.API_SECRET)
        bm = BinanceSocketManager(client)
        intervals_names = [i.name for i in self.exchange.intervals.all()]
        stream_names = ["{}@kline_{}".format(self.market.name.lower(), i) for i in intervals_names]
        conn_key = bm.start_multiplex_socket(stream_names, self._process_message)
        self.log(str(self.__class__) + " start")
        bm.start()

    def _process_message(self, msg):
        data = msg['data']
        k = data['k']
        symbol_param, interval_param = k['s'], k['i']
        open_at = dt.fromtimestamp(int(k['t']) / 1000, tz=pytz.UTC)
        close_at = dt.fromtimestamp(int(k['T']) / 1000, tz=pytz.UTC)
        event_time = dt.fromtimestamp(int(data['E']) / 1000, tz=pytz.UTC)
        open_price, close_price, high_price, low_price = k['o'], k['c'], k['h'], k['l']
        volume, closed = k['v'], k['x']

        log = "[{}]({}): ({} - {}) {} o: {}, c: {}, h: {}, l: {}, v: {}, closed: {}".format(
            symbol_param, interval_param, open_at, close_at, event_time,
            open_price, close_price, high_price, low_price,
            volume, closed)

        self.log(log)

        candle, _ = Candle.objects.get_or_create(
            exchange_market=self.exchange_market,
            interval=Interval.objects.get(name=interval_param),
            open_at=open_at, close_at=close_at
        )
        Candle.objects.filter(id=candle.pk).update(
            open=open_price, close=close_price, high=high_price, low=low_price,
            volume=volume, closed=closed
        )


class MarketFetcherService(Service):
    exchange, market = Exchange.objects.get(name='Binance'), Market.objects.get(name='BTCUSDT')
    exchange_market = ExchangeMarket.objects.get(exchange=exchange, market=market)
    command = None

    def __init__(self, *args, **kwargs):
        self.command = kwargs['command']
        kwargs.pop('command', None)
        super(MarketFetcherService, self).__init__(*args, **kwargs)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),
                               facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.INFO)

    def run(self):
        self.command.stdout.write(self.command.style.SUCCESS("Service run."))
        client = Client(keys.API_KEY, keys.API_SECRET)
        bm = BinanceSocketManager(client)
        intervals_names = [i.name for i in self.exchange.intervals.all()]
        stream_names = ["{}@kline_{}".format(self.market.name.lower(), i) for i in intervals_names]
        conn_key = bm.start_multiplex_socket(stream_names, self._process_message)
        bm.start()

    def _process_message(self, msg):
        data = msg['data']
        k = data['k']
        symbol_param, interval_param = k['s'], k['i']
        open_at = dt.fromtimestamp(int(k['t']) / 1000, tz=pytz.UTC)
        close_at = dt.fromtimestamp(int(k['T']) / 1000, tz=pytz.UTC)
        event_time = dt.fromtimestamp(int(data['E']) / 1000, tz=pytz.UTC)
        open_price, close_price, high_price, low_price = k['o'], k['c'], k['h'], k['l']
        volume, closed = k['v'], k['x']

        log = "[{}]({}): ({} - {}) {} o: {}, c: {}, h: {}, l: {}, v: {}, closed: {}".format(
            symbol_param, interval_param, open_at, close_at, event_time,
            open_price, close_price, high_price, low_price,
            volume, closed)

        candle, _ = Candle.objects.get_or_create(
            exchange_market=self.exchange_market,
            interval=Interval.objects.get(name=interval_param),
            open_at=open_at, close_at=close_at
        )
        Candle.objects.filter(id=candle.pk).update(
            open=open_price, close=close_price, high=high_price, low=low_price,
            volume=volume, closed=closed
        )


class Command(BaseCommand):
    help = 'Manages market fetcher service'

    def add_arguments(self, parser):
        parser.add_argument('command', type=str)

    def handle(self, *args, **options):
        cmd = options['command']

        # service = MarketFetcherService('market_fetcher_service', pid_dir='/tmp', command=self)
        service = MarketFetcher(command=self)

        if cmd == 'start':
            service.start()
        else:
            raise CommandError('Unknown command "%s".' % cmd)
        """
        elif cmd == 'stop':
            self.stdout.write(self.style.SUCCESS("Service stopped."))
            service.stop()
        elif cmd == 'status':
            if service.is_running():
                self.stdout.write(self.style.SUCCESS("Service is running."))
            else:
                self.stdout.write(self.style.SUCCESS("Service is not running."))
        """
