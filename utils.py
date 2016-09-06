# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import urllib
import os

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