from django.db import models


class MarketType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'market_market_type'


class Market(models.Model):
    name = models.CharField(max_length=50, unique=True)
    market_type = models.ForeignKey(MarketType, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Interval(models.Model):
    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Exchange(models.Model):
    name = models.CharField(max_length=250, unique=True)
    intervals = models.ManyToManyField(Interval)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ExchangeMarket(models.Model):
    exchange = models.ForeignKey(Exchange, related_name='exchange_markets', on_delete=models.PROTECT)
    market = models.ForeignKey(Market, related_name='exchange_markets', on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'market_exchange_market'


class Candle(models.Model):
    exchange_market = models.ForeignKey(ExchangeMarket, on_delete=models.PROTECT)
    interval = models.ForeignKey(Interval, on_delete=models.PROTECT)

    open_at = models.DateTimeField()
    close_at = models.DateTimeField()

    open = models.FloatField(null=True)
    close = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)

    volume = models.FloatField(null=True)
    closed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
