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
        self.iterval = None # TODO

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
    def dimensionless_length(self):
        """a method which is a metric for dimensionless length"""
        return self.__len__()/self.low

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

    def __getitem__(self, attr):
        if attr == 'close':
            return self.close
        elif attr == 'open':
            return self.open
        elif attr == 'low':
            return self.low
        elif attr == 'high':
            return self.high
        elif attr == 'prev':
            return self.prev
        elif attr == 'next':
            return self.next
        else:
            raise NotImplementedError(f"the '{attr}' is not a valid access key")

    def _compare_seq(
        self,
        how,
        other_candle_direction,
        this_field='close',
        other_field='open',
        n=1
        ):
        """Determines whether this field of this candle is smallert than other field
        of nth next or prev candle sequentially. Sequentially mean this should stand for
        all prev or next candles
        """
        assert n >= 1
        this = self
        while n >= 1:
            if this._compare(how, other_candle_direction, this_field, other_field, 1) is False:
                return False
            this = this[other_candle_direction]
            n = n - 1
        return True

    def _compare(
        self,
        how,
        other_candle_direction,
        this_field='close',
        other_field='open',
        n=1
        ):
        """Determines whether this field of this candle is smallert than other field
        of nth next candle
        """
        assert n >= 1
        assert how in ('<', '>', '<=', '>=')
        assert other_candle_direction in ('prev', 'next')
        other = self.__getitem__(other_candle_direction)
        while n >=1:
            if other is None or other is numpy.nan:
                return False
            else:
                nth_other_field = other[other_field]
                other = other[other_candle_direction]
                n -= 1
        if how == '<':
            return self[this_field] < nth_other_field
        elif how == '>':
            return self[this_field] > nth_other_field
        else:
            raise NotImplementedError(f"Not implemented for the give how='{how}'")

    def has_higher_close_than_nth_next_close(self, n, seq=False):
        if seq is False:
            return self._compare('>', 'next', 'close', 'close', n)
        else:
            return self._compare_seq('>', 'next', 'close', 'close', n)

    def has_lower_close_than_nth_next_close(self, n, seq=False):
        if seq is False:
            return self._compare('<', 'next', 'close', 'close', n)
        else:
            return self._compare_seq('<', 'next', 'close', 'close', n)

    def has_higher_close_than_nth_prev_close(self, n, seq=False):
        if seq is True:
            return self._compare('>', 'prev', 'close', 'close', n)
        else:
            return self._compare_seq('>', 'prev', 'close', 'close', n)

    def has_lower_close_than_nth_prev_close(self, n, seq=False):
        if seq is True:
            return self._compare('<', 'prev', 'close', 'close', n)
        else:
            return self._compare_seq('<', 'prev', 'close', 'close', n)

    @property
    def is_swing_high(self):
        """returns True if the candle is a swing high"""
        return self._compare_seq('>', 'next', 'high', 'high', 2) and\
            self._compare_seq('>', 'prev', 'high', 'high', 2)

    @property
    def is_swing_low(self):
        """returns True if the candle is a swing low"""
        return self._compare_seq('<', 'next', 'low', 'low', 2) and\
            self._compare_seq('<', 'prev', 'low', 'low', 2)

    @property
    def is_support(self):
        """returns True if the candle close price is a support (minimum of next and prev closes)"""
        return self.has_lower_close_than_nth_next_close(1) and self.has_lower_close_than_nth_prev_close(1)

    @property
    def is_resistance(self):
        """returns True if the candle close price is a resistance (maximum of next and prev closes)"""
        return self.has_higher_close_than_nth_next_close(1) and self.has_higher_close_than_nth_prev_close(1)

    def support_level(self, m :int):
        level = 0
        assert m >= 2
        for i in range(1, m):
            if (
                self.has_lower_close_than_nth_next_close(i)
                and
                self.has_lower_close_than_nth_prev_close(i)
            ):
                level = i
            else:
                return level
        return level

    def resistance_level(self, m: int):
        level = 0
        assert m >= 2
        for i in range(1, m):
            if (
                self.has_higher_close_than_nth_next_close(i)
                and
                self.has_higher_close_than_nth_prev_close(i)
            ):
                level = i
            else:
                return level
        return level

    def has_lower_low_than_prev_low(self):
        """Checks wether the low of this candlestick is smaller than the low of its previous"""
        return self._compare('<', 'prev', 'low', 'low', 1)

    def has_higher_high_than_prev_high(self):
        """Checks wether the high of this candlestick is bigger than the high of its previous"""
        return self._compare('>', 'prev', 'high', 'high', 1)

    def has_lower_low_than_next_low(self):
        """Checks wether the low of this candlestick is smaller than low of the its next"""
        return self._compare('<', 'next', 'low', 'low', 1)

    def has_higher_high_than_next_high(self):
        """Checks wether the high of this candlestick is bigger than high of the its next"""
        return self._compare('>', 'next', 'high', 'high', 1)

    def has_prev_lower_low_than_its_prev_low(self):
        """checks wether the low of this candlestick is smaller than second previous candlestick low"""
        if self.prev.prev is None or self.prev.prev is numpy.nan:
            return False
        else:
            return self.prev.has_lower_low_than_prev_low()

    def has_prev_higher_high_than_its_prev_high(self):
        """checks wether the high of this candlestick is bigger than second previous candlestick high"""
        if self.prev.prev is None or self.prev.prev is numpy.nan:
            return False
        else:
            return self.prev.has_higher_high_than_prev_high()

    def has_next_lower_low_than_its_next_low(self):
        """checks wether the low of this candlestick is smaller than second next candlestick"""
        if self.next.next is None or self.next.next is numpy.nan:
            return False
        else:
            return self.next.has_lower_low_than_next_low()

    def has_next_higher_high_than_its_next_high(self):
        """checks wether the high of this candlestick is bigger than second next candlestick high"""
        if self.next.next is None or self.next.next is numpy.nan:
            return False
        else:
            return self.next.has_higher_high_than_next_high()

    @property
    def length_ratio_prev(self):
        """finds the ratio of lenght of this candle relative to prev candle"""
        if self.prev is None or self.prev is numpy.nan:
            return None
        else:
            if self.prev.__len__() == 0:
                return -1
            else:
                return self.__len__() / self.prev.__len__()

    @property
    def length_ratio_next(self):
        """finds the ratio of lenght of this candle relative to next candle"""
        if self.next is None or self.next is numpy.nan:
            return None
        else:
            if self.next.__len__() == 0:
                return -1
            else:
                return self.__len__() / self.next.__len__() 

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

    def __str__(self):
        return str(self.sorted_ohlc)


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
                candle.prev = None
                if row['Candlesticks_next'] == numpy.nan:
                    candle.next = None
            elif index == len(self._df) - 1:
                candle.prev = row['Candlesticks_prev']
                candle.next = None
                if row['Candlesticks_next'] == numpy.nan:
                    candle.prev = None
            else:
                candle.next = row['Candlesticks_next']
                candle.prev = row['Candlesticks_prev']
            self._df.loc[index, 'Candlesticks'] = candle
        del self._df['Candlesticks_prev']
        del self._df['Candlesticks_next']

    def set_df(self, df):
        self._df = df
        self._df['datex'] = df.index
        self._df.sort_values('datex', ascending=True, inplace=True)
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
        self._df['is_hollow'] = self._df['Candlesticks'].apply(lambda item: item.is_hollow)
        self._df['is_filled'] = self._df['Candlesticks'].apply(lambda item: item.is_filled)
        self._df['min_o1'] = self._df['Candlesticks'].apply(lambda item: item.min_o1)
        self._df['min_o2'] = self._df['Candlesticks'].apply(lambda item: item.min_o2)
        self._df['max_o1'] = self._df['Candlesticks'].apply(lambda item: item.max_o1)
        self._df['max_o2'] = self._df['Candlesticks'].apply(lambda item: item.max_o2)
        self._df['is_support'] = self._df['Candlesticks'].apply(lambda item: item.is_support)
        self._df['is_resistance'] = self._df['Candlesticks'].apply(lambda item: item.is_resistance)
        self._df['support_level'] = self._df['Candlesticks'].apply(lambda item: item.support_level(1000))
        self._df['resistance_level'] = self._df['Candlesticks'].apply(lambda item: item.resistance_level(1000))
        self._df['dimensionless_length'] = self._df['Candlesticks'].apply(lambda item: item.dimensionless_length)
        self._df['length_ratio_prev'] = self._df['Candlesticks'].apply(lambda item: item.length_ratio_prev)
        self._df['length_ratio_next'] = self._df['Candlesticks'].apply(lambda item: item.length_ratio_next)
        self._df['is_swing_high'] = self._df['Candlesticks'].apply(lambda item: item.is_swing_high)
        self._df['is_swing_low'] = self._df['Candlesticks'].apply(lambda item: item.is_swing_low)

    def to_values(self):
        return self._df.to_dict(orient='records')

    def __getitem__(self, key):
        return self._df[key]

    @property
    def columns(self):
        return self._df.columns
