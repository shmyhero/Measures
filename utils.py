# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import urllib
import os
from  talib.abstract import *

# YAHOO_URL = "http://table.finance.yahoo.com/table.csv?s=ibm&d=6&e=22&f=2006&g=d&a=11&b=16&c=1991&ignore=.csv"
YAHOO_URL = "http://table.finance.yahoo.com/table.csv?s="

def download_stock_data(stock, start_date, end_date):
    url = YAHOO_URL+stock+"&d=11&e=31&f=2015&g=d&a=0&b=1&c=1990&ignore=.csv"
    print url
    try:
        file = urllib.urlopen(url)
        filedata = file.read()
        file.close()
    except Exception, e:
        print "download file from site failed: ", url
        return ''

    csv_name = stock+".csv"
    if os.path.isfile(csv_name):
        os.remove(csv_name)

    with open(csv_name, 'w') as csvfile:
        csvfile.write(filedata)

    return filedata

def cbk(a, b, c):
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    if c > 0:
        print '%.2f%%' % per
    else:
        print '█',

def download_csv_file(stock, start_date='', end_date=''):
    url = YAHOO_URL+stock+"&d=11&e=31&f=2015&g=d&a=0&b=1&c=1990&ignore=.csv"
    print url

    csv_name = stock+".csv"
    if os.path.isfile(csv_name):
        os.remove(csv_name)

    try:
        urllib.urlretrieve(url, csv_name, cbk)
    except Exception, e:
        print "download file from site failed: ", url
        return ''

    return csv_name

def load_data(csv_file):
    df = pd.read_csv(csv_file, index_col='Date', parse_dates=True)
    df = df.reindex(df.index[::-1])
    df.columns = [item.lower() for item in df.columns]
    return df

def show_aroon_plt(df, length, dropna=False):
    ardf = AROON(df, timeperiod=25)
    if dropna:
        ardf = ardf.dropna()
    headdf = ardf.head(length)
    headdf.plot()

def aroon_buy(df):
    # 1, up line >70
    # 2, down line < 50
    # 3, up line cross down line
    ardf = AROON(df, timeperiod=25)
    ardf = ardf.dropna()
    ardf["updown"]=ardf.aroonup-ardf.aroondown
    ardf["lastupdown"]=ardf.updown.shift(1)
    rdf = ardf[(ardf.aroonup>70) & (ardf.aroondown<50) & (ardf.updown > 0) & (ardf.lastupdown < 0)]
    return rdf

def aroon_sell(df):
    # 1, down line >70
    # 2, up line < 50
    # 3, down line cross up line
    ardf = AROON(df, timeperiod=25)
    ardf = ardf.dropna()
    ardf["updown"]=ardf.aroonup-ardf.aroondown
    ardf["lastupdown"]=ardf.updown.shift(1)
    rdf = ardf[(ardf.aroondown>70) & (ardf.aroonup<50) & (ardf.updown < 0) & (ardf.lastupdown > 0)]
    return rdf

def expected_revenue(df, indice, day, price_name="adj close"):
    sdf = df.shift(-day)
    df = df.ix[indice]
    sdf = sdf.ix[indice]
    # df["revenue"] = (sdf.close / df.close - 1) * 100
    df["revenue"] = (sdf[price_name] / df[price_name] - 1) * 100
    return df.ix[:,["revenue"]]


def show_aroon_revenue_plt(df, isup=True, days=10, price_name="adj close"):
    # show the mean revenue of %days aroon up/down indicator.
    indice = []
    if isup:
        indice = aroon_buy(df).index
    else:
        indice = aroon_sell(df).index
    revenue = [expected_revenue(df, indice, day, price_name).mean().ix[0,0] for day in range(1, days+1)]
    df2 = pd.DataFrame({'revenue':revenue}, index=range(1, len(revenue)+1))
    df2.plot()
    print df2
    return df2

def win_rate(df, indice, day, base_rate=0.1, price_name="adj close"):
    erdf = expected_revenue(df, indice, day, price_name)
    return 1.0 * len(erdf[erdf.revenue>base_rate]) / len(erdf)

def show_aroon_win_rate_plt(df, isup=True, days=10, base_rate=0.1, price_name="adj close"):
    # show the win rate of %days aroon up/down indicator.
    # if down, win means expected rate < base_rate
    indice = []
    if isup:
        indice = aroon_buy(df).index
    else:
        indice = aroon_sell(df).index
    winrate = [win_rate(df, indice, day, base_rate, price_name) for day in range(1, days+1)]
    df2 = pd.DataFrame({'winrate':winrate}, index=range(1, len(winrate)+1))
    if not isup:
        df2 = 1 - df2
    df2.plot()
    print df2
    return df2