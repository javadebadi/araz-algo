from datetime import date, datetime
from .base import BaseDMList

class OHLCDM:
    """A class to models symbols OHLC
    
    OHLC is an apprevation for Open-High-Low-Close prices
    during a timeframe of trading
    """

    def __init__(
        self,
        symbol:str,
        interval:str
        ) -> None:
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.start_unix_time = None
        self.start_datetime = None
        self.amount = None
        self.volume = None
        self.interval = interval
        self.symbol = symbol

    def set(self, data:dict) -> None:
        self.set_open(data.get('open'))
        self.set_close(data.get('close'))
        self.set_high(data.get('high'))
        self.set_low(data.get('low'))
        self.set_amount(data.get('amount'))
        self.set_volume(data.get('volume'))
        self.set_start_unix_time(data.get('start_unix_time'))

    def set_open(self, value) -> None:
        self.open = float(value)

    def set_close(self, value) -> None:
        self.close = float(value)

    def set_low(self, value) -> None:
        self.low = float(value)

    def set_high(self, value) -> None:
        self.high = float(value)

    def set_amount(self, value) -> None:
        self.amount = float(value)

    def set_volume(self, value) -> None:
        self.volume = float(value)

    def set_start_unix_time(self, value) -> None:
        self.start_unix_time = int(value)
        self.start_datetime = datetime.utcfromtimestamp(self.start_unix_time)


    def __str__(self) -> str:
        s = ""
        s += f"symbol = {self.symbol}\n"
        s += f"interval = {self.interval}\n"
        s += f"low = {self.low}\n"
        s += f"high = {self.high}\n"
        s += f"open = {self.open}\n"
        s += f"close = {self.close}\n"
        s += f"volume = {self.volume}\n"
        s += f"amount = {self.amount}\n"
        s += f"start_unix_time = {self.start_unix_time}\n"
        s += f"start_datetime = {self.start_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"
        return s


class OHLCDMList(BaseDMList):
    def __init__(self, values:list = None):
        super().__init__()
