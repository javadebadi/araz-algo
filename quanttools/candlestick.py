"""A Candlestick class
"""
from pandas.core.series import Series
from pandas.core.frame import DataFrame
import pandas
import numpy


class CandleStickNode:
    """A class for candlestick used in tradings"""

    def __init__(
        self,
        open: float=None,
        high: float=None,
        low: float=None,
        close: float=None,
        volume: float=None
        ) -> None:
        if open is not None:
            self.set_ohlc(open, high, low, close)
            self.volume = volume
        else:
            self.set_none()
        self.prev = None
        self.next = None

    def sorted_ohlc(self):
        return self.sorted_ohlc

    def ohlc(self):
        return (self.open, self.high, self.low, self.close)

    def set_ohlc(self, open: float, high: float, low:float, close:float):
        if not (
            (isinstance(open, float) or isinstance(open, int))
            and
            (isinstance(high, float) or isinstance(high, int))
            and
            (isinstance(low, float) or isinstance(low, int))
            and
            (isinstance(close, float) or isinstance(close, int))
            ):
            raise TypeError('all values given to ohlc method must be float or integer')
        assert (low <= close and low <= high and low <= open)
        assert (high >= close and high >= open )
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.sorted_ohlc = sorted(self.ohlc())

    def set_none(self):
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.sorted_ohlc = None


    # computational methods
    def __len__(self):
        return self.high - self.low

    @property
    def upper_shadow(self):
        return self.sorted_ohlc[3] - self.sorted_ohlc[2]

    @property
    def lower_shadow(self):
        return self.sorted_ohlc[1] - self.sorted_ohlc[0]

    @property
    def real_body(self):
        return self.sorted_ohlc[2] - self.sorted_ohlc[1]

    @property
    def is_hollow(self):
        return self.close > self.open

    @property
    def is_filled(self):
        return self.open > self.close

    def __truediv__(self, other):
        """Overloaded / operator 
        
        The method returns the ratio of lengths of LHS Candlestick
        to RHS candlestick object

        >>> c = CandlestickNode(100, 500, 0, 200)
        >>> d = CandlestickNode(1000, 5000, 0, 2000)
        >>> d / c
        10.0
        """
        return self.__len__() / other.__len__()

    def __floordiv__(self, other):
        """Overloaded // operator 
        
        The method returns the ratio of lengths of LHS Candlestick
        to RHS candlestick object

        >>> c = CandlestickNode(100, 500, 0, 200)
        >>> d = CandlestickNode(1000, 5000, 0, 2000)
        >>> d // c
        10
        """
        return self.__len__() // other.__len__()

    def has_lower_low_than_prev_low(self):
        """Checks wether the low of this candlestick is smaller than the low of its previous"""
        if self.prev is None:
            return False
        else:
            return self.low <= self.prev.low

    def has_higher_high_than_prev_high(self):
        """Checks wether the high of this candlestick is bigger than the high of its previous"""
        if self.prev is None:
            return False
        else:
            return self.high >= self.prev.high

    def has_lower_low_than_next_low(self):
        """Checks wether the low of this candlestick is smaller than low of the its next"""
        if self.next is None:
            return False
        else:
            return self.low <= self.next.low

    def has_higher_high_than_next_high(self):
        """Checks wether the high of this candlestick is bigger than high of the its next"""
        if self.next is None:
            return False
        else:
            return self.high >= self.next.high


    def has_prev_lower_low_than_its_prev_low(self):
        """checks wether the low of this candlestick is smaller than second previous candlestick low"""
        if self.prev.prev is None:
            return False
        else:
            return self.prev.has_lower_low_than_prev_low()

    def has_prev_higher_high_than_its_prev_high(self):
        """checks wether the high of this candlestick is bigger than second previous candlestick high"""
        if self.prev.prev is None:
            return False
        else:
            return self.prev.has_higher_high_than_prev_high()

    def has_next_lower_low_than_its_next_low(self):
        """checks wether the low of this candlestick is smaller than second next candlestick"""
        if self.next.next is None:
            return False
        else:
            return self.next.has_lower_low_than_next_low()

    def has_next_higher_high_than_its_next_high(self):
        """checks wether the high of this candlestick is bigger than second next candlestick high"""
        if self.next.next is None:
            return False
        else:
            return self.prev.has_higher_high_than_next_high()

    @property
    def min_o1(self):
        return self.has_lower_low_than_next_low() and self.has_lower_low_than_prev_low()

    @property
    def max_o1(self):
        return self.has_higher_high_than_prev_high() and  self.has_higher_high_than_next_high()

    @property
    def min_o2(self):
        return self.min_o1 and self.has_next_lower_low_than_its_next_low() and self.has_prev_lower_low_than_its_prev_low()

    @property
    def max_o2(self):
        return self.max_o1 and self.has_prev_higher_high_than_its_prev_high() and self.has_next_higher_high_than_its_next_high()


class CandlestickTimesSeries:
    """
    >>> import pandas as pd
    >>> df = pd.read_csv('BTC-USD.csv', index_col=0, parse_dates=True).dropna()
    >>> c = CandlestickTimesSeries(df)
    >>> c = CandlestickTimesSeries([2])
    Traceback (most recent call last):
    ...
    AssertionError
    >>> c = CandlestickTimesSeries(df)
    >>> c.add_candlestick_features()
    >>> assert 'upper_shadow' in c.df.columns
    """
    def __init__(self, df: DataFrame=None) -> None:
        if df is not None:
            assert isinstance(df, pandas.core.frame.DataFrame)
            assert set(['open', 'high', 'low', 'close']).issubset(set(df.columns))
        self.set_df(df)

    # def append(self, candlestick):
    #     if self.ts:
    #         self.ts[-1].next = candlestick
    #         self.ts.append(cand)

    @property
    def df(self):
        return self._df

    def _set_candles_linked_list(self):
        self._df['Candlesticks_prev'] = self._df['Candlesticks'].shift(1)
        self._df['Candlesticks_next'] = self._df['Candlesticks'].shift(-1)
        for index, row in self._df.iterrows():
            candle = row['Candlesticks']
            if index == 0:
                candle.next = row['Candlesticks_next']
            elif index == len(self._df) - 1:
                candle.prev = row['Candlesticks_prev']
            else:
                candle.next = row['Candlesticks_next']
                candle.prev = row['Candlesticks_prev']
            self._df.loc[index:index+1, 'Candlesticks'] = candle
        del self._df['Candlesticks_prev']
        del self._df['Candlesticks_next']

    def set_df(self, df):
        self._df = df
        self._df['Candlesticks'] = df.apply(
            lambda row: CandleStickNode(row['open'], row['high'], row['low'], row['close'], row['volume']),
            axis=1
            )
        self._set_candles_linked_list()

    def add_candlestick_features(self):
        self._df['length'] = self._df['Candlesticks'].apply(lambda item: item.__len__())
        self._df['upper_shadow'] = self._df['Candlesticks'].apply(lambda item: item.upper_shadow)
        self._df['lower_shadow'] = self._df['Candlesticks'].apply(lambda item: item.lower_shadow)
        self._df['real_body'] = self._df['Candlesticks'].apply(lambda item: item.real_body)
        self.df['is_hollow'] = self._df['Candlesticks'].apply(lambda item: item.is_hollow)
        self._df['is_filled'] = self._df['Candlesticks'].apply(lambda item: item.is_filled)
        self._df['min_o1'] = self._df['Candlesticks'].apply(lambda item: item.min_o1)
        self._df['min_o2'] = self._df['Candlesticks'].apply(lambda item: item.min_o2)
        self._df['max_o1'] = self._df['Candlesticks'].apply(lambda item: item.max_o1)
        self._df['max_o2'] = self._df['Candlesticks'].apply(lambda item: item.max_o2)
        # add longness
        # self._df['longness'] = numpy.nan
        # self._df['longness'][1:] = self._df['Candlesticks'][1:] / self._df['Candlesticks'].shift(1)[1:]
        # self._df['longness_signed'] = self._df.apply(lambda item: int(item['is_hollow'])*item['longness'] - int(item['is_filled'])*item['longness'], axis=1)
        # for index in range(len(self._df)):
        #     if index == 0:
        #         self._df['longness'].iloc[0] = None
        #     else:
        #         self._df['longness'].iloc[index] = self._df['Candlesticks'].iloc[index]/self._df['Candlesticks'].iloc[index-1]

    def to_values(self):
        return self._df.to_dict(orient='records')
        
