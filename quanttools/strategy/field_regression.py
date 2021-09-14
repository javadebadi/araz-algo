from datetime import date, datetime
import time
from sklearn.linear_model import LinearRegression
from data_access import CandleStickDA
from datetime import datetime
from pandas import Timestamp
import pandas as pd
import numpy as np
from utils import convert_UTC_datetime_to_unix_time


def reg_model(
    symbol,
    field,
    interval,
    n_last=48,
    n_next=12,
    t_0=None,
    return_type='df'
):
    if t_0 is None:
        t_0 = int(time.time())
    da = CandleStickDA()
    df = da.get_df(symbol, interval, t_0)
    assert(len(df)>=n_last)
    # train data
    X = df['start_unix_time'][-n_last:].values.reshape(n_last,1)
    y = df[field][-n_last:].values.reshape(n_last,1)
    # build regression model
    reg = LinearRegression()
    reg.fit(X, y)
    # predict
    next_times = np.array([t_0 + i*30*60 for i in range(1, n_next+1)]).reshape(n_next, 1)
    # all times
    all_times = X.tolist() + next_times.tolist()
    next_preds = reg.predict(all_times).tolist()
    all_times = [item[0] for item in all_times]
    all_datetimes = [datetime.utcfromtimestamp(item) for item in all_times]
    next_preds = [item[0] for item in next_preds]
    if return_type == 'tuple':
        return list(zip(all_times, next_preds))
    if return_type == 'df':
        return pd.DataFrame(data={'start_datetime':all_datetimes, field: next_preds})
    
        
    
