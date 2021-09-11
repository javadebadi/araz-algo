
import os
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    and_,
    )
from sqlalchemy.sql import (
    insert,
    select,
    update,
    )
import pandas as pd
from website.settings import BASE_DIR

CONNECTION_STRING = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

engine = create_engine(CONNECTION_STRING)

metadata = MetaData(engine)



class SymbolDA:
    """A class to handle data operations in 'symbol' table
    """
    
    def insert_or_update_if_exists(self, values: list):
        assert isinstance(values, list)
        
        with engine.begin() as con:
            symbol_table = Table('symbol', metadata, autoload=True, autoload_with=engine)
            for value in values:
                select_stmt = select([symbol_table]).where(symbol_table.columns.symbol==value['symbol'])
                if con.execute(select_stmt).fetchall():
                    stmt = update(symbol_table).where(symbol_table.columns.symbol==value['symbol']).values(value)
                else:
                    stmt = insert(symbol_table).values([value])
                con.execute(stmt)


    def get_watch_lists(self):
        view = f"""SELECT symbol FROM v_watch_list"""
        with engine.begin() as con:
            return con.execute(view).fetchall()


class OHLCDA:
    """A class to handle data operations on 'ohlc' table
    """

    def insert_or_update_if_exists(self, values: list):
        assert isinstance(values, list)
        
        with engine.begin() as con:
            ohlc_table = Table('ohlc', metadata, autoload=True, autoload_with=engine)
            for value in values:
                select_stmt = select([ohlc_table]).where(
                    and_(
                        ohlc_table.columns.symbol==value['symbol'],
                        ohlc_table.columns.start_datetime==value['start_datetime']
                    )
                )
                if con.execute(select_stmt).fetchall():
                    stmt = update(ohlc_table).where(
                        and_(
                            ohlc_table.columns.symbol==value['symbol'],
                            ohlc_table.columns.start_datetime==value['start_datetime']
                            )
                        ).values(value)
                else:
                    stmt = insert(ohlc_table).values([value])
                con.execute(stmt)

    def get_watch_lists(self):
        view = f"""SELECT symbol FROM v_watch_list"""
        with engine.begin() as con:
            return [row['symbol'] for row in con.execute(view).fetchall()]
                
    def get_min_unix(self):
        pass  # TO DO


class CandleStickDA:
    """A class to handle candlestick table data"""
    def insert_or_update_if_exists(self, values: list):
        assert isinstance(values, list)
        
        with engine.begin() as con:
            candlestick_table = Table('candlestick', metadata, autoload=True, autoload_with=engine)
            for value in values:
                select_stmt = select([candlestick_table]).where(
                        candlestick_table.columns.ohlc_id==value['ohlc_id']
                )
                if con.execute(select_stmt).fetchall():
                    stmt = update(candlestick_table).where(
                        candlestick_table.columns.ohlc_id==value['ohlc_id']
                    ).values(value)
                else:
                    stmt = insert(candlestick_table).values([value])
                con.execute(stmt)

    def get_query_string_of_raw_symbol_interval_data(self, symbol, interval):
        query_string = f"""SELECT id AS ohlc_id,
                                  symbol,
                                  interval,
                                  open,
                                  high,
                                  low,
                                  close,
                                  volume,
                                  amount,
                                  start_datetime,
                                  start_unix_time
                            FROM ohlc
                            where symbol = '{symbol}' and interval = '{interval}'
                            ORDER BY start_datetime"""
        return query_string
    
    def get_raw_df(self, symbol, interval):
        return pd.read_sql(
            self.get_query_string_of_raw_symbol_interval_data(symbol, interval),
            con=CONNECTION_STRING
            )

    def get_df(self, symbol, interval, to_start_unix_time=None):
        return pd.read_sql(
            f"""SELECT  ohlc_id,
                        symbol,
                        start_unix_time,
                        start_datetime,
                        interval,
                        open,
                        high,
                        low,
                        close,
                        volume,
                        amount,
                        min_o1,
                        max_o1,
                        min_o2,
                        max_o2
                    FROM v_candlestick
                    WHERE 
                        symbol = '{symbol}'
                        and
                        interval = '{interval}'
                        {'' if (to_start_unix_time is None) else f'and start_unix_time < {to_start_unix_time} ' }
            """,
            con=CONNECTION_STRING
        )


class OrderDA:
    """A class to handle Order tables"""
    def insert_or_update_if_exists(self, values: list):
        assert isinstance(values, list)
        
        with engine.begin() as con:
            order_table = Table('order', metadata, autoload=True, autoload_with=engine)
            for value in values:
                select_stmt = select([order_table]).where(
                    order_table.columns.order_id==value['order_id']
                )
                if con.execute(select_stmt).fetchall():
                    stmt = update(order_table).where(
                    order_table.columns.order_id==value['order_id']
                ).values(value)
                else:
                    stmt = insert(order_table).values([value])
                con.execute(stmt)