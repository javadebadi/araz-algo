from django import db
from django.db import models
from django.db.models.fields import AutoField
from django.utils import tree
from .symbol import Symbol
from django.contrib.auth.models import User

class FeeCurrency(models.Model):
    fee_currency = models.CharField(
        max_length=10,
        primary_key=True
        )

    class Meta:
        db_table = 'fee_currency'
        verbose_name = 'Fee Currency'
        verbose_name_plural = 'Fee Currencies'

class Order(models.Model):
    order_id = models.CharField(
        max_length=32,
        primary_key=True
        ) # order id such as 6138721b3baec40006d43dea
    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.PROTECT,
        db_column='symbol'
        ) # such as 'ADA-USDT'
    op_type = models.CharField(
        max_length=10
    ) # such as 'DEAL'
    type = models.CharField(
        max_length=16
    ) # such as 'limit'
    side = models.CharField(
        max_length=10
    ) # trading side which is either buy or sell
    price = models.FloatField() # the price
    size = models.FloatField() # the size (number of currencies or size of the deal)
    funds = models.FloatField() # the value of associated funds which is still needed for the deal to be fillted (not dealed)
    deal_funds = models.FloatField() # the value of order which is filled
    deal_size = models.FloatField() # the size which is filled
    stp = models.CharField(max_length=16, null=True, blank=True, default='')
    time_in_force = models.CharField(max_length=3, null=True, blank=True)
    cancel_after = models.IntegerField(null=True, blank=True)
    STOP_CHOICES = (
        ('loss', 'loss'),
        ('entry', 'entry'),
    )
    stop = models.CharField(max_length=16, choices=STOP_CHOICES, null=True, blank=True)
    stop_price = models.FloatField(null=True, blank=True)
    stop_triggered = models.BooleanField(null=True, blank=True)
    post_only = models.BooleanField(null=True, blank=True, default=False)
    hidden = models.BooleanField(null=True, blank=True, default=False)
    iceberg = models.BooleanField(null=True, blank=True, default=False)
    visible_size = models.FloatField(null=True, blank=True, default=0)
    channel = models.CharField(max_length=16, null=True, blank=True, default='') # such as 'WEB' , 'API'
    client_oid = models.CharField(max_length=32, null=True, blank=True, default='')
    remark = models.CharField(max_length=64, null=True, blank=True, default='')
    tags = models.CharField(max_length=64, null=True, blank=True, default='')
    fee = models.FloatField() # the amount of fee
    fee_currency = models.ForeignKey(
        FeeCurrency,
        on_delete=models.PROTECT,
        db_column='fee_currency'
    )
    is_active = models.BooleanField() # order status, true and false.
    # If true, the order is active, if false, the order is fillled or cancelled
    cancel_exist = models.BooleanField(
    ) # whether the order is canceller or not if true the cancel exists
    created_at = models.IntegerField(
        null=True, blank=True
    ) # a unix time in which the order is created
    TRADE_TYPE_CHOICES = (
        ('TRADE', 'Spot Trading'), 
        ('MARGIN_TRADE', 'Margin Trading')
    )
    trade_type = models.CharField(
        max_length=16,
        choices=TRADE_TYPE_CHOICES
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        db_column='user_id'
    )
    
    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ('created_at', )

    def __str__(self) -> str:
        return self.order_id