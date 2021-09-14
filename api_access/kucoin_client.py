import time
from datetime import datetime
from kucoin.client import Client

from config import (
    API_SECRET,
    API_PASSPHRASE,
    API_KEY
)

class KucoinClient(Client):
    def __init__(self) -> None:
        super().__init__(API_KEY, API_SECRET, API_PASSPHRASE)

    def _translate_order_dict(self, result):
        result['order_id'] = result['id']
        result['op_type'] = result['opType']
        result['deal_funds'] = result['dealFunds']
        result['deal_size'] = result['dealSize']
        result['stop_price'] = result['stopPrice']
        result['stop_triggered'] = result['stopTriggered']
        result['fee_currency'] = result['feeCurrency']
        result['time_in_force'] = result['timeInForce']
        result['post_only'] = result['postOnly']
        result['hidden'] = result['hidden']
        result['iceberg'] = result['iceberg']
        result['is_active'] = result['isActive']
        result['created_at'] = result['createdAt']
        result['trade_type'] = result['tradeType']
        result['cancel_exist'] = result['cancelExist']
        result['client_oid'] = result['clientOid']
        result['visible_size'] = result['visibleSize']
        result['cancel_after'] = result['cancelAfter']
        return result

    def get_orders(
        self,
        symbol=None,
        status=None,
        side=None,
        order_type=None,
        start=None,
        end=None,
        page=None,
        limit=None
        ):
        if status is None:
            results_active = super().get_orders(
                symbol=symbol,
                status='active',
                side=side,
                order_type=order_type,
                start=start,
                end=end,
                page=page,
                limit=limit
                )['items']
            results_done= super().get_orders(
                symbol=symbol,
                status='done',
                side=side,
                order_type=order_type,
                start=start,
                end=end,
                page=page,
                limit=limit
                )['items']
        new_results = []
        for result in results_active:
            new_results.append(self._translate_order_dict(result))
        for result in results_done:
            new_results.append(self._translate_order_dict(result))
        return new_results

    def __str__(self) -> str:
        return self.symbol
