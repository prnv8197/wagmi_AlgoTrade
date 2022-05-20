#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 13:14:11 2021

@author: pranav.atulya
"""

import yfinance as yf
import pandas as pd

from utils.dydx import setup_dydx


def getOHLC(stock, period, interval, suffix = ""):
    stock = stock+suffix
    tickr = yf.Ticker(stock)
    hist = tickr.history(period, interval)
    hist=hist.drop(['Dividends', 'Stock Splits'], axis=1)
    return hist

def getFromDydx(client, market, interval):
    candles = client.public.get_candles(
    market=market,
    resolution=interval,
    )
    df = pd.DataFrame(candles.data['candles'])
    # Return the reverse (latest time at the bottom)
    return df[::-1]

if __name__ == "__main__":
    client = setup_dydx()
    from dydx3.constants import MARKET_BTC_USD
    getFromDydx(client, MARKET_BTC_USD, '1MIN')







#-------------- Set Paramenters--------------#

# stock = 'NDX'
# period = '2y' # '1mo'. '6mo'
# interval = '1d' #“1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo” 
# suffix = ""
# ohlc = getOHLC(stock, period, interval, suffix = '')
# # print(ohlc[0:len(ohlc)-24])
# print(ohlc['Close'][-1])
# print(ohlc['Close'][0])
# print((ohlc['Close'][-1] - ohlc['Close'][0])/)
# ohlc.to_csv('/Users/pranav.atulya/Documents/GitHub/Backtesting_ver1/dataFiles/axisbank_1h_6mo.csv')