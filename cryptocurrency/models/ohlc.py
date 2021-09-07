"""The model for OHLC"""
from django.db import models
from .watch_list import WatchList

class OHLC(models.Model):
    symbol = models.ForeignKey(
        WatchList,
        on_delete=models.CASCADE,
        db_column='symbol'
    )
    start_unix_time = models.IntegerField()
    open =  models.FloatField()
    close = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    amount = models.FloatField()
    volume = models.FloatField()
    start_datetime = models.DateTimeField()
    interval = models.CharField(max_length=16)


    def __str__(self):
        return f"{self.symbol.__str__()} ({self.interval}) -  {self.start_datetime.strftime('%Y-%m-%d %H:%M:%S')}"


    class Meta:
        db_table = 'ohlc'
        verbose_name = 'OHLC'
        verbose_name_plural = 'OHLCs'
        ordering = (
            'symbol',
            '-start_datetime',
            )
        unique_together = ('start_datetime', 'symbol')