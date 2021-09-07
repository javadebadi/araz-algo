import os
from quanttools import candlestick
from br import (
    SymbolBR,
    OHLCBR,
    CandleStickBR,
)
import time
from datetime import (
    datetime,
    timedelta,
)
from multiprocessing import Process

    
import logging
logging.basicConfig(filename='myapp.log', level=logging.INFO, format='%(asctime)s %(message)s')

MINUTE = 60
HOUR = 60*MINUTE
DAY = 24*HOUR

START_TIME = datetime(2021,9,6,0,31,0)
timedelta(minutes=30)


def switch_bool(bool_var):
    bool_var = not bool_var

def _run_symbols_job():
    while True:
        if datetime.now() < START_TIME:
            continue
        symbol_br = SymbolBR()
        symbol_br.insert_or_update_symbol_table()
        time.sleep(DAY)


def _run_ohlc_job():
    logging.warning('Started OHLC reading job from API ...')  # will print a message to the console
    while True:
        if datetime.now() < START_TIME:
            continue
        ohlc_br = OHLCBR()
        ohlc_br.insert_or_update_ohlc_table(
            interval='30min',
            start=int(time.time()-365*DAY),
            end=int(time.time()))
        # add candlestick features to candlestick table
        # for TRX-USDT
        candlestick_br = CandleStickBR('TRX-USDT', '30min')
        candlestick_br.get_raw_df()
        candlestick_br.add_features()
        candlestick_br.insert_or_update_candlestick_table()
        candlestick_br = CandleStickBR('VRA-USDT', '30min')
        candlestick_br.get_raw_df()
        candlestick_br.add_features()
        candlestick_br.insert_or_update_candlestick_table()
        time.sleep(HOUR)

        
def _run_django():
    os.system("python manage.py runserver")

def run():
    """a fucntion to run all """
    logging.info('Started')
    # run django server
    p_django = Process(target=_run_django)
    p_django.start()
    # run symbols job
    p_symbols_job = Process(target=_run_symbols_job)
    p_symbols_job.start()
    # run ohlc job
    p_ohlc_job = Process(target=_run_ohlc_job)
    p_ohlc_job.start()


    # join jobs
    p_django.join()
    p_symbols_job.join()
    p_ohlc_job.join()
    logging.info('Finished')


if __name__ == '__main__':
    run()
    # _run_ohlc_job()