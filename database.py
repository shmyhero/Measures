# -*- coding: utf-8 -*-
# from os import getenv
import pymssql
import pandas as pd

server = "thvm-chinap3.chinacloudapp.cn"
port = "888"
user = "tradehero_sa"
password = "__sa90070104th__"
datebase = "CFD"

def load_recent_data(number=1000, securityid=34858):
    with pymssql.connect(server, user, password, datebase, port=port) as conn:
        # with conn.cursor(as_dict=True) as cursor:
            # cursor.execute("select * from information_schema.tables")     #all table
        df = pd.read_sql('select top(%d) * from QuoteHistory where SecurityId = %d'% (number, securityid), con=conn, index_col='Time', parse_dates=True)
        df["price"] = (df["Bid"]+df["Ask"])/2
        df2 = df.groupby(pd.TimeGrouper('10S'))
        df3 = df2.max()
        df3["high"]=df3.price
        df3["low"]=df2.min().price
        df3 = df3.fillna(method="pad")
        return df3

# print load_recent_data(1000)

def create_record_table():
    #todo
