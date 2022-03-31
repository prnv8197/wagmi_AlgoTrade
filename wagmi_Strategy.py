#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 18:27:49 2022

@author: pranav.atulya
"""
import pandas as pd
from getData import getOHLC
from OLS import OLS_max, regression_channel
from datetime import datetime
from getIndicators import *


def MyStrategy1(crypto_asset, p_interval, p_period, s_interval, s_period):
   
    flag_long = False
    flag_short = False
    
    price = getOHLC(crypto_asset, period = p_period, interval = p_interval)
    price = getBollingerBands(price)
    price = getMACD(price)
    price['50SMA'] = price['Close'].rolling(window = 50).mean()   
    macd_mean = price['signal_line'].mean()
    macd_dev = price['signal_line'].std()
    if(price['50SMA'][-1] > price['Upper Band'][-1] and price['signal_line'][-1] < macd_mean-1*macd_dev):
        
        price_s = getOHLC(crypto_asset, period = s_period, interval = s_interval)
        flag_s = price_s['Close'].rolling(window = 50).mean()[-1] < price_s['Close'][-1]
        price = regression_channel(price)
        rc_cross = price['UC'][-1] < price['Close'][-1]
        if(rc_cross and flag_s):
            flag_long = True
        return flag_long
        
    if(price['50SMA'][-1] < price['Lower Band'][-1] and price['signal_line'][-1] > macd_mean+1*macd_dev): 
        
        price_s = getOHLC(crypto_asset, period = s_period, interval = s_interval)
        flag_s = price_s['Close'].rolling(window = 50).mean()[-1] > price_s['Close'][-1]
        price = regression_channel(price)
        rc_cross = price['LC'][-1] > price['Close'][-1]
        if(rc_cross and flag_s):
            flag_short = True
        return flag_short
        
    return False
        

# print(MyStrategy1('ETH-USD', '5m', '1mo', '1m', '1mo'))