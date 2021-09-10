from .da import engine
import logging
from sqlalchemy.exc import OperationalError

v_watch_list = \
"""
CREATE VIEW v_watch_list AS
SELECT symbol
FROM symbol
JOIN watch_list
USING (symbol)"""

v_candlestick = \
"""
CREATE VIEW v_candlestick AS
SELECT  ohlc_id,
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
FROM ohlc
JOIN candlestick
    ON ohlc.id == candlestick.ohlc_id
ORDER BY symbol, start_datetime
"""

views_names = [
    'v_watch_list',
    'v_candlestick'
    ]
SQL_views = [
    v_watch_list,
    v_candlestick
    ]

def drop_views():
    """A function to drop all views to replace them"""
    for view_name in views_names:
        logging.info(f"DA: views: started to drop the {view_name}")
        with engine.begin() as con:
            try:
                con.execute(f"DROP VIEW {view_name}")
                logging.info("DA: views: droped the ")
            except OperationalError as e:
                logging.info(f"DA: view: {str(e)}")

def create_views():
    # first drop thev view if they exists
    drop_views()
    # start to create views
    logging.info("DA: started to create views in database")
    for view in SQL_views:
        with engine.begin() as con:
            stmts = view.split(';')
            for stmt in stmts:
                con.execute(stmt)
    logging.info("DA: 2 views are created in database")