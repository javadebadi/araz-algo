from quanttools import CandlestickTimesSeries
from data_access import CandleStickDA
import logging
from data_models import (
    CandleStickDMList,
    CandleStickDM,
)

class CandleStickBR:

    def __init__(
        self,
        symbol,
        interval
        ):
        self.symbol = symbol
        self.interval = interval
        self.candlestick_ts = None

    def get_raw_df(self):
        logging.info(f"CandleStick: started to get raw OHLC data for {self.symbol} at {self.interval}")
        da = CandleStickDA()
        df = da.get_raw_df(self.symbol, self.interval)
        self.candlestick_ts = CandlestickTimesSeries(df)
        logging.info(f"CandleStick: created a candlestick times series for OHLC raw data ")

    def add_features(self):
        self.candlestick_ts.add_candlestick_features()
        logging.info(f"CandleStick: Added candlestick features")

    def insert_or_update_candlestick_table(self):
        logging.info(f"CandleStick: created a CandleStickDMList object")
        candlestick_dm_list_obj = CandleStickDMList()
        candlestick_dm_list_obj.reset()
        for value in self.candlestick_ts.to_values():
            candlestick_dm_obj = CandleStickDM()
            candlestick_dm_obj.set(value)
            candlestick_dm_list_obj.append(candlestick_dm_obj)

        da = CandleStickDA()
        logging.warning(f'CandleStick: Started to fill candlestick table')
        da.insert_or_update_if_exists(candlestick_dm_list_obj.to_list_of_values())
        logging.warning(f'CandleStick: Finished filling of candlestick table in database')

    