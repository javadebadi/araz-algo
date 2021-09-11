"""A module to build strategy for buy and sell based on linear regression

The strategy is implemented for 30min base and limited number of coins

The strategy looks for past mins and maxes of 30mic candles and result
in a position for just next 30min

"""

import logging

from datetime import date, datetime
import time
from sklearn.linear_model import LinearRegression
from data_access import CandleStickDA
from datetime import datetime
from pandas import Timestamp
from utils import convert_UTC_datetime_to_unix_time

def is_almost_equal(value_1:float, value_2:float, error=0.01):
    if abs(value_1-value_2) < error:
        return True
    else:
        return False

from api_access import KucoinClient

client = KucoinClient()

class RegressionSupportResistanceStrategy:
    def __init__(self, symbol:str, interval:str) -> None:
        assert interval in ['30min']
        self.symbol = symbol
        self.interval = interval
        self.apply_datetime = None
        self.apply_unix_time = None
        self.df = None

    def set_apply_unix_time(self, unix_time:float=None) -> None:
        self.apply_unix_time = unix_time
        if self.interval == '30min':
            self.apply_datetime = datetime.utcfromtimestamp(self.apply_unix_time).replace(microsecond=0, second=0)
            if self.apply_datetime.minute < 30:
                self.apply_datetime = self.apply_datetime.replace(minute=0)
            else:
                self.apply_datetime = self.apply_datetime.replace(minute=30)
            self.new_apply_unix_time = convert_UTC_datetime_to_unix_time(self.apply_datetime)
        else:
            raise NotImplementedError("Not implemented YET")

    def load_historical_data(self) -> None:
        if self.apply_datetime is None:
            raise ValueError("you need to set apply_datetime before loading historical data")
        da = CandleStickDA()
        self.df = da.get_df(self.symbol, self.interval, self.apply_unix_time)

    def set_strategy_hyperparameters(
        self,
        support_train_data_size:int,
        resistance_train_data_size:int,
        min_kind = 'min_o1',
        max_kind = 'max_o1'
        ):
        self.support_train_data_size = support_train_data_size
        self.resistance_train_data_size = resistance_train_data_size
        self.min_kind = min_kind
        self.max_kind = max_kind


    def fit(self):
        df_support = self.df[ self.df[self.min_kind] == True][['low', 'start_unix_time']][-self.support_train_data_size:]
        X_supprt = df_support['start_unix_time'].values.reshape(len(df_support),1)
        y_supprt = df_support['low'].values.reshape(len(df_support),1)
        df_resistance = self.df[ self.df[self.max_kind] == True][['high', 'start_unix_time']][-self.resistance_train_data_size:]
        X_resistance = df_resistance ['start_unix_time'].values.reshape(len(df_resistance),1)
        y_resistance = df_resistance ['high'].values.reshape(len(df_resistance),1)
        self.support_reg = LinearRegression()
        self.support_reg.fit(X_supprt, y_supprt)
        self.resistance_reg = LinearRegression()
        self.resistance_reg.fit(X_resistance, y_resistance)

    def predict(self):
        self.predictions = {
            "support": {
                "start_datetime": datetime.utcfromtimestamp(self.apply_unix_time),
                "start_unix_time":self.apply_unix_time,
                "value": self.support_reg.predict([[self.apply_unix_time]]).reshape(-1,1).flatten()[0]
            },
            "resistance": {
                "start_datetime": datetime.utcfromtimestamp(self.apply_unix_time),
                "start_unix_time":self.apply_unix_time,
                "value": self.resistance_reg.predict([[self.apply_unix_time]]).reshape(-1,1).flatten()[0]
            },
        }
        return  self.predictions


    def take_positions(self):
        self.fit()
        self.predict()
        logging.warning("Started to take positions")
        last_low = self.df[-1:]['low'].values[0]
        last_close = self.df[-1:]['close'].values[0]
        support_value = self.predictions['support']['value']
        resistance_value = self.predictions['resistance']['value']

        if is_almost_equal(last_low, support_value, 0.005):
            logging.warning("The recent low and support are nearly equal")
            logging.warning(f"POSTION: BUY {self.symbol} at {support_value}")
            # kucoin
            try:
                # order_id = client.create_limit_order(f'{self.symbol}', client.SIDE_BUY, str(round(support_value,4)), '20')
                # print(order_id)
                logging.warning(f"SET BUY: SUCCESS")
                time.sleep(1.5*60*60)
            except:
                logging.error("NO MONEY ....")
                pass
        else:
            if last_low < support_value:
                logging.warning(f"POSITION: *DANGER* if things go bad sell some {self.symbol} to stop loss")
            else:
                if is_almost_equal(last_close, resistance_value, 0.01):
                    logging.warning(f"POSITION: SELL {self.symbol} at {resistance_value}")
                try:
                    # order_id = client.create_limit_order(f'{self.symbol}', client.SIDE_SELL, str(round(resistance_value,4)), '20')
                    # print(order_id)
                    logging.warning(f"SET SELL: SUCCESS")
                    time.sleep(1.5*60*60)
                except:
                    logging.error("NO COIN ....")
                    pass
                else:
                    logging.warning(f"POSITION: Do not trade {self.symbol} yet ... NO BUY... NO SELL ..")
            return None

    def __str__(self) -> str:
        s = f" ===== SYMBOL = {self.symbol} at {self.interval} intervals ===== \n"
        if self.apply_unix_time is not None:
            s += f'original unix time = {self.apply_unix_time}\n'
            s += f'original unix time (UTC datetime) = {datetime.utcfromtimestamp(self.apply_unix_time)}\n'
            s += f'smallest 30min datetime = {self.apply_datetime}\n'
            s += f'unix time for smallest 30min datetime = {self.new_apply_unix_time}\n'
            s += f'datetime of unix time for smallest 30min datetime = {datetime.utcfromtimestamp(self.new_apply_unix_time)}\n'
        if self.df is not None:
            s += f"size of historical dataframe = {len(self.df)}\n"
        return s

