"""The model for symbols"""
from django.db import models

class Symbol(models.Model):
    symbol = models.CharField(
        max_length=16,
        primary_key=True
    )

    def __str__(self):
        return str(self.symbol)

    class Meta:
        db_table = 'symbol'
        verbose_name = 'Symbol'
        verbose_name_plural = 'Symbols'
        ordering = ('symbol', )