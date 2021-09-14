from bokeh.models.annotations import Legend
from django.http.response import HttpResponse
from django.shortcuts import render
import pandas as pd
from math import pi
from bokeh.plotting import figure, output_file, show
from website.settings import BASE_DIR
from bokeh.embed import file_html
from bokeh.resources import CDN
import numpy as np
from quanttools.strategy import reg_model

import os

CONNECTION_STRING = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

class LineTS:
    
    def __init__(self, start_timestamp, end_timestamp, start_y, end_y, freq='30min', shift=0):
        self.xs = pd.date_range(start=start_timestamp, end=end_timestamp, freq='30min')
        self.ys = np.linspace(start_y, end_y, len(self.xs)) + shift
        
    def to_df(self, col_name='value', index_name='start_datetime'):
        self.df = pd.DataFrame(data={col_name:self.ys}, index=self.xs)
        self.df.index.name = index_name
        return self.df
        
    def __str__(self):
        return str(self.xs) + "\n" + str(self.ys)
    

class LineSegmentTS:
    
    def __init__(self, timestamps, ys, freq='30min', shift=0):
        self.m = len(timestamps)
        self.lines = []
        for i in range(self.m-1):
            line = LineTS(timestamps[i], timestamps[i+1], ys[i], ys[i+1], freq=freq, shift=shift)
            self.lines.append(line)
            
    def to_df(self, col_name='value', index_name='start_datetime'):
        list_of_dfs = []
        for index, line in enumerate(self.lines):
            if index == self.m-1:
                list_of_dfs.append(line.to_df(col_name, index_name))
            else:
                list_of_dfs.append(line.to_df(col_name, index_name)[:-1])
        return pd.concat(list_of_dfs)
        
                              

# line_seg = LineSegmentTS([df.index[5], df.index[7], df.index[9]], [10,20,40])
# line_seg.to_df()

from quanttools import RegressionTimeStampsTS

# Create your views here.
def main(request, symbol, min=None, max=None, minsize=None, maxsize=None):
    
    if min is None:
        min_kind = 'min_o2'
    else:
        min_kind = min

    if max is None:
        max_kind = 'max_o1'
    else:
        max_kind = max

    if minsize is None:
        minsize = 12
    else:
        minsize = minsize

    if maxsize is None:
        maxsize = 30
    else:
        maxsize = maxsize

    

    df = pd.read_sql(
        sql=f"""SELECT * FROM ohlc
                JOIN candlestick
                ON ohlc.id = candlestick.ohlc_id
                where symbol = '{symbol}' and interval='30min' ORDER BY start_datetime""",
        con=CONNECTION_STRING)[-200:]
    df["start_datetime"] = pd.to_datetime(df["start_datetime"])
    df.set_index(df['start_datetime'], inplace=True)

    window_size = 12
    # df['support'] = df['low'].rolling(window=window_size).min()
    df['resistance'] = df['high'].rolling(window=window_size).max()
    # new_df = df[df['min_o1']==True].copy()
    # new_df= LineSegmentTS(new_df['start_datetime'].to_list(), new_df['low'].to_list()).to_df('support', 'start_datetime')
    # new_df["start_datetime"] = pd.to_datetime(new_df.index)

    reg_ts = RegressionTimeStampsTS(
        df,
        bool_filter_col=min_kind,
        objective_col='low',
        train_data_size=minsize,
        freq='30min'
        )
    new_df = reg_ts.fit_interpolate_extraploate()
    new_df['min_o1_reg_support'] = new_df['reg_pred']

    reg_ts = RegressionTimeStampsTS(
        df,
        bool_filter_col=max_kind,
        objective_col='high',
        train_data_size=maxsize,
        freq='30min'
        )
    new_max_df = reg_ts.fit_interpolate_extraploate()
    new_max_df['max_o1_reg_support'] = new_max_df['reg_pred']


    # field regression
    low_reg_df = reg_model(symbol, 'low', '30min', 24, 12)
    high_reg_df = reg_model(symbol, 'high', '30min', 24, 12)


    TOOLTIPS = [
    ("index", "$index"),
    # ("desc", "@desc"),
    ]


    # print(new_df)
    # new_df['support'] = new_df['low'].rolling(window=2).min()
    # df['support'] = (df['low']*df['min_o1']).rolling(window=window_size).sum()/df['min_o1'].rolling(window=window_size).sum()

    inc = df.close > df.open
    dec = df.open > df.close
    w = 20*60*1000 # half day in ms

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = f"{symbol} Candlestick",  tooltips=TOOLTIPS)
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.start_datetime, df.high, df.start_datetime, df.low, color="black")
    p.vbar(df.start_datetime[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.start_datetime[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    # p.hbar(0.075, 0.01, df.start_datetime[inc], df.start_datetime[inc], fill_color="#F2583E", line_color="black")
    # p.line([df.start_datetime.min(), df.start_datetime.max()], [0.075, 0.075], line_width=2, legend_label='support')
    # p.line(df.start_datetime, df.support, line_width=2, legend_label='support')
    # p.line(new_df.start_datetime, new_df.support, line_width=2, legend_label='support')
    p.line(new_df.start_datetime, new_df.min_o1_reg_support, line_width=2, legend_label='support')
    p.line(low_reg_df.start_datetime, low_reg_df.low, line_width=2, legend_label='lows regression', line_color='#44FF77')
    # p.line(new_df.start_datetime, new_df.support, line_width=2, legend_label='support')
    # p.line(df.start_datetime, df.resistance, line_width=2, legend_label='resistance',  line_color="#ff5555")
    p.line(new_max_df.start_datetime, new_max_df.max_o1_reg_support, line_width=2, legend_label='resistance', line_color="#ff5555")
    p.line(high_reg_df.start_datetime, high_reg_df.high, line_width=2, legend_label='high regression', line_color='#FF3311')
    

    return HttpResponse(file_html(p, CDN, "my plot"))
    