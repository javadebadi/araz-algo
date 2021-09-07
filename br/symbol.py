from api_access import KucoinClient
from data_access import (
    OHLCDA,
    SymbolDA,
)
from data_models import (
    SymbolDM,
    SymbolDMList,
    OHLCDM,
    OHLCDMList,
    ohlc,
    watch_list,
)
import logging


class SymbolBR:
    """A class to handle business rules for about symbol model
    """

    class api:

        client = KucoinClient()

        def get_symbols_list(self):
            return self.client.get_symbols()

    def insert_or_update_symbol_table(self):
        values = self.api().get_symbols_list()
        symbol_dm_list_obj = SymbolDMList(values)
        da = SymbolDA()
        da.insert_or_update_if_exists(symbol_dm_list_obj.to_list_of_values())

class OHLCBR:
    """A class to handle business rules of the OHLC model
    """
    def __init__(self) -> None:
        pass

    class api:

        client = KucoinClient()

        def get_ohlc_data(self, symbol:str , interval:str, start:int=None, end:int=None):
            """
            Args:
                symbol (str): Name of symbol e.g. KCS-BTC
                interval (str): type of symbol, type of candlestick patterns: 1min, 3min, 5min, 15min, 30min, 1hour, 2hour,
                    4hour, 6hour, 8hour, 12hour, 1day, 1week
                start (int): Start time as unix timestamp (optional) default start of day in UTC
                end (int): End time as unix timestamp (optional) default now in UTC
            """
            klines = self.client.get_kline_data(symbol, interval, start, end)
            values = []

            for index, kline in enumerate(klines):
                value = dict()
                value['start_unix_time'] = klines[index][0]
                value['open'] = klines[index][1]
                value['close'] = klines[index][2]
                value['high'] = klines[index][3]
                value['low'] = klines[index][4]
                value['amount'] = klines[index][5]
                value['volume'] = klines[index][6]
                values.append(value)
            return values

    def _get_watch_list_data_from_api(self):
        logging.warning('Started to get list of symbols in watch list (OHLCBR class)')
        da = OHLCDA()
        watch_list_symbols = da.get_watch_lists()
        logging.warning('Finished getting list of symbols in watch list (OHLCBR class)')
        return watch_list_symbols

    def insert_or_update_ohlc_table(self, interval, start=None, end=None):
        ohlc_dm_list_obj = OHLCDMList()
        ohlc_dm_list_obj.reset()
        for symbol in self._get_watch_list_data_from_api():
            logging.warning(f'Started to get {symbol} OHLC data from API at {interval} interval')
            values = self.api().get_ohlc_data(symbol, interval, start, end)
            for value in values:
                ohlc_obj = OHLCDM(symbol, interval)
                ohlc_obj.set(value)
                ohlc_dm_list_obj.append(ohlc_obj)
        da = OHLCDA()
        logging.warning(f'Started adding watch list recent OHLC data to database')
        da.insert_or_update_if_exists(ohlc_dm_list_obj.to_list_of_values())
        logging.warning(f'Finished adding watch list recent OHLC data to database')

