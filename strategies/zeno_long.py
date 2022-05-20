#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 20 02:25:44 2022

@author: pranav.atulya
"""

# Basic Initial strat
# Indicators used: Bollinger bands, MACD, Simple moving average, OLS regression channel 
# Data feed: Close price, period: last 1 month, interval: 5min(primary), 1min(confirmation) (May change later based on backtest results)
# Entry condition; BUY/GoLong: (50SMA > UBB) and (MACD_FastLine < MACD_FastLine_mean - MACD_FastLine_stdev) 
# Entry condition cofirmation; BUY/GoLong: (Close_1min > 50SMA_1min)
# Entry condition; SELL/GoShort: *exact opposite of the buy conditions.

# strat1 takes two dataframes, one for each interval(primary and confirmation); 
# It requires the dataframes to have the close price and all the indicator values as separate columns

def strat1(price_primary, price_confirmation):
    macd_mean = price_primary['signal_line'].mean()
    macd_dev = price_primary['signal_line'].std()
    
    if(price_primary['SMA50'][-1] > price_primary['Upper Band'][-1] and price_primary['signal_line'][-1] < price_primary['MACD_mean'][-1]-1*price_primary['MACD_dev'][-1]):
        
        if(price_confirmation['SMA50'][-1] < price_confirmation['Close'][-1]):
            return True
        else:
            return False
    else:
        return False
        
        