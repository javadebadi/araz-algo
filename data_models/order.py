"""Data models for order table"""
from .base import BaseDMList


class OrderDM:
    def __init__(self):
        pass

    def set(self, data: dict):
        self.symbol = data.get('symbol')
        self.order_id = data.get('order_id')
        self.op_type = data.get('op_type')
        self.side = data.get('side')
        self.price = float(data.get('price'))
        self.size = float(data.get('size'))
        self.funds = float(data.get('funds'))
        self.type = data.get('type')
        self.deal_funds = float(data.get('deal_funds'))
        self.deal_size = float(data.get('deal_size'))
        self.stp = data.get('stp', None)
        self.stop = data.get('stop', None)
        self.stop_price = float(data.get('stop_price', None))
        self.stop_triggered = bool(data.get('stop_triggered'))
        self.fee = float(data.get('fee'))
        self.fee_currency = data.get('fee_currency')
        self.time_in_force = data.get("time_in_force", None)
        self.post_only = bool(data.get('post_only'))
        self.hidden = bool(data.get('hidden', None))
        self.iceberg = bool(data.get('iceberg', None))
        self.visible_size = float(data.get('visible_size', None))
        self.cancel_after = int(data.get('cancel_after')) if (data.get('cancel_after', None) is not None) else None
        self.channel = data.get('channel', None)
        self.client_oid = data.get('client_oid', None)
        self.remark = data.get('remark', None)
        self.tags = data.get('tags', None)
        self.is_active = bool(data.get('is_active', None))
        self.created_at =  int(data.get('create_at')) if (data.get('create_at', None) is not None) else None
        self.trade_type = data.get('trade_type')
        self.cancel_exist = bool(data.get('cancel_exist'))
        self.user_id = 1 # TO DO TODO

    def __str__(self) -> str:
        return self.symbol


class OrderDMList(BaseDMList):
    def __init__(self, values:list = None):
        self.collection = None
        if values is not None:
            self.set(values)

    def set(self, values: list):
        self.collection = []
        for value in values:
            order_dm_obj = OrderDM()
            order_dm_obj.set(value)
            self.collection.append(order_dm_obj)
