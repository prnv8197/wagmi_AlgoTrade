#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 12:28:45 2022

@author: pranav.atulya
"""

import pandas as pd
import statsmodels.formula.api as sm
import yfinance as yf
from getIndicators import *
from getData import *



def OLS_max(ohlc):
    ohlc1 = pd.DataFrame(ohlc[-24:])
    ohlc1['Step'] = [i for i in range(len(ohlc1['Close']))]
    result = sm.ols(formula="Close ~ Step", data=ohlc1).fit()
    ohlc1['Predicted'] = result.params['Intercept'] + result.params['Step']*ohlc1['Step']
    ohlc1['Residual%'] = abs(((ohlc1['Predicted'] - ohlc1['Close'])/ohlc1['Close'])*100)
    return max(ohlc1['Residual%'])

def regression_channel(ohlc):
    ohlc1 = pd.DataFrame(ohlc[-24:])
    ohlc1['Step'] = [i for i in range(len(ohlc1['Close']))]
    result = sm.ols(formula="Close ~ Step", data=ohlc1).fit()
    ohlc1['Predicted'] = result.params['Intercept'] + result.params['Step']*ohlc1['Step']
    ohlc1['UC'] = ohlc1['Predicted'] + 1 * ohlc1['Close'].std()
    ohlc1['LC'] = ohlc1['Predicted'] - 1 * ohlc1['Close'].std()
    return ohlc1

# stock = 'BRIATNNIA'
# period = '2d' # '1mo'. '6mo'
# interval = '15m' #“1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo” 
# suffix = ""
# ohlc = getOHLC(stock, period, interval, suffix = '.NS')[:-24]
# ohlc = ohlc.drop(['High', 'Low'], axis=1)
# rc = regression_channel(ohlc)
# print(rc)