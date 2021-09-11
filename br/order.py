from data_access import OrderDA
import logging
from data_models import (
    OrderDM,
    OrderDMList,
)
from api_access import KucoinClient

class OrderBR:

    def __init__(self):
        pass

    class api:

        client = KucoinClient()

        def get_orders(self, symbol=None, status=None, limit=500):
            order_records = self.client.get_orders(symbol=symbol, status=status, limit=limit)
            return order_records


    def insert_or_update_order_table(self, symbol=None, status=None, limit=500):
        order_dm_list_obj = OrderDMList()
        order_dm_list_obj.reset()
        for value in self.api().get_orders(symbol=symbol, status=status, limit=limit):
            order_dm_obj = OrderDM()
            order_dm_obj.set(value)
            order_dm_list_obj.append(order_dm_obj)

        da = OrderDA()
        da.insert_or_update_if_exists(order_dm_list_obj.to_list_of_values())

    