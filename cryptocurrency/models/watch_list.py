"""The model for WatchList"""
from django.db import models
from django.contrib.auth.models import User
from .symbol import Symbol

class WatchList(models.Model):
    symbol = models.OneToOneField(
        Symbol,
        primary_key=True,
        on_delete=models.CASCADE,
        db_column='symbol'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user_id'
    )

    def __str__(self):
        return self.symbol.__str__()

    class Meta:
        db_table = 'watch_list'
        verbose_name = 'Watch List'
        verbose_name_plural = 'Watch List'