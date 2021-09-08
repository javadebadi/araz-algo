from django.db import models
from .ohlc import OHLC

class CandleStick(models.Model):
    ohlc = models.OneToOneField(
        OHLC,
        primary_key=True,
        db_column='ohlc_id',
        on_delete=models.CASCADE
    )
    length = models.FloatField()
    min_o1 = models.BooleanField() # order 1 minimum
    min_o2 = models.BooleanField() # order 2 minimum
    max_o1 = models.BooleanField(null=True) # order 1 maximum
    max_o2 = models.BooleanField(null=True) # order 2 maximum


    class Meta:
        db_table = 'candlestick'
        verbose_name = 'CandleStick'
        verbose_name_plural = 'CandleSticks'
    
    def __str__(self):
        return self.ohlc.__str__()


