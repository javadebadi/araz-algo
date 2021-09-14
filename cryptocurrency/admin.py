from django.contrib import admin

from .models import (
    Symbol,
    WatchList,
    OHLC,
    CandleStick,
    FeeCurrency,
    Order,
    Position,
)
from cryptocurrency import models

# Register your models here.
@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    model = Symbol
    list_display = ('symbol', )
    search_fields = ('symbol', )

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    model = WatchList
    list_display = ('symbol', 'user')

@admin.register(OHLC)
class OHLCAdmin(admin.ModelAdmin):
    model = OHLC
    list_display = ('symbol', 'start_datetime', 'open', 'high', 'low', 'close')
    list_filter = ('symbol', 'start_datetime')
    search_fields = ('symbol', 'close', 'low', 'volume')


@admin.register(CandleStick)
class CandleStickAdmin(admin.ModelAdmin):
    model = CandleStick
    list_display = ('ohlc', 'min_o1', 'min_o2', 'max_o1', 'max_o2', 'length')

@admin.register(FeeCurrency)
class FeeCurrencyAdmin(admin.ModelAdmin):
    model = FeeCurrency
    list_display = ('fee_currency', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('order_id', 'price', 'size', 'funds', 'deal_funds', 'deal_size', 'fee')
    # list_display = ('order_id', 'symbol', 'user_id', 'price', 'size', 'funds', 'fee', 'deal_size', 'deal_funds')
    list_filter = ('symbol', 'is_active')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    model = Position
    list_display = ('position_id', 'price', 'size', 'symbol', 'strategy')
    list_filter = ('symbol', 'strategy')

