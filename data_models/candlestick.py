"""Data models for candlestick table"""
from .base import BaseDMList

class CandleStickDM:
    def __init__(self):
        pass

    def set(self, data: dict):
        self.ohlc_id = data.get('ohlc_id')
        self.length = data.get('length')
        self.min_o1 = data.get('min_o1')
        self.min_o2 = data.get('min_o2')
        self.max_o1 = data.get('max_o1')
        self.max_o2 = data.get('max_o2')

    def __str__(self) -> str:
        s = ""
        s += f"length = {self.length}\n"
        s += f"min_o1 = {self.min_o1}\n"
        s += f"min_o2 = {self.min_o2}\n"
        s += f"max_o1 = {self.max_o1}\n"
        s += f"max_o2 = {self.max_o2}\n"
        return s


class CandleStickDMList(BaseDMList):
    def __init__(self, values:list = None):
        self.collection = None
        if values is not None:
            self.set(values)

    def set(self, values: list):
        self.collection = []
        for value in values:
            candlestick_obj = CandleStickDM()
            candlestick_obj.set(value)
            self.collection.append(candlestick_obj)