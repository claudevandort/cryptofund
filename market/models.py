from django.db import models


class MarketType(models.Model):
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'market_market_type'


class Market(models.Model):
    name = models.CharField(max_length=50)
    market_type = models.ForeignKey(MarketType, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Exchange(models.Model):
    name = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ExchangeMarket(models.Model):
    exchange = models.ForeignKey(Exchange, related_name='exchange_markets', on_delete=models.PROTECT)
    market = models.ForeignKey(Market, related_name='exchange_markets', on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'market_exchange_market'

