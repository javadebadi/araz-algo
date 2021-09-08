from bokeh.models.annotations import Legend
from django.http.response import HttpResponse
from django.shortcuts import render
import pandas as pd
from math import pi
from bokeh.plotting import figure, output_file, show
from website.settings import BASE_DIR
from bokeh.embed import file_html
from bokeh.resources import CDN

import os

CONNECTION_STRING = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')



# Create your views here.
def main(request, symbol):
    

    df = pd.read_sql(
        sql=f"""SELECT * FROM ohlc
                JOIN candlestick
                ON ohlc.id = candlestick.ohlc_id
                where symbol = '{symbol}' ORDER BY start_datetime""",
        con=CONNECTION_STRING)[-300:-100]
    df["start_datetime"] = pd.to_datetime(df["start_datetime"])

    window_size = 12
    df['support'] = df['low'].rolling(window=window_size).min()
    df['resistance'] = df['high'].rolling(window=window_size).max()
    new_df = df[df['min_o1']==True]
    # new_df['support'] = new_df['low'].rolling(window=2).min()
    # df['support'] = (df['low']*df['min_o1']).rolling(window=window_size).sum()/df['min_o1'].rolling(window=window_size).sum()

    inc = df.close > df.open
    dec = df.open > df.close
    w = 20*60*1000 # half day in ms

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,hover"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title = f"{symbol} Candlestick")
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.start_datetime, df.high, df.start_datetime, df.low, color="black")
    p.vbar(df.start_datetime[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.start_datetime[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    # p.hbar(0.075, 0.01, df.start_datetime[inc], df.start_datetime[inc], fill_color="#F2583E", line_color="black")
    # p.line([df.start_datetime.min(), df.start_datetime.max()], [0.075, 0.075], line_width=2, legend_label='support')
    p.line(df.start_datetime, df.support, line_width=2, legend_label='support')
    # p.line(new_df.start_datetime, new_df.support, line_width=2, legend_label='support')
    p.line(df.start_datetime, df.resistance, line_width=2, legend_label='resistance',  line_color="#ff5555")
    

    return HttpResponse(file_html(p, CDN, "my plot"))
    