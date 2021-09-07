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


    class Meta:
        db_table = 'candlestick'
        verbose_name = 'CandleStick'
        verbose_name_plural = 'CandleSticks'
    
    def __str__(self):
        return self.ohlc.__str__()


