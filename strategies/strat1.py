#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 01:25:32 2022

@author: pranav.atulya
"""

# Basic Initial strat
# Indicators used: Bollinger bands, MACD, Simple moving average, OLS regression channel 
# Data feed: Close price, period: last 1 month, interval: 5min(primary), 1min(confirmation) (May change later based on backtest results)
# Entry condition; BUY/GoLong: (50SMA > UBB) and (MACD_FastLine < MACD_FastLine_mean - MACD_FastLine_stdev) and (Close > UC)
# Entry condition cofirmation; BUY/GoLong: (Close_1min > 50SMA_1min)
# Entry condition; SELL/GoShort: *exact opposite of the buy conditions.

# strat1 takes two dataframes, one for each interval(primary and confirmation); 
# It requires the dataframes to have the close price and all the indicator values as separate columns

def strat1(price_primary, price_confirmation, i):
    # macd_mean = price_primary['signal_line'].mean()
    # macd_dev = price_primary['signal_line'].std()
    
    if(price_primary['SMA50'][i] > price_primary['Upper Band'][i]): #and price_primary['signal_line'][i] < price_primary['MACD_mean'][i]-1*price_primary['MACD_dev'][i] and price_primary['UC'][i] < price_primary['Close'][i]):
        return True
        
        # if(price_confirmation['SMA50'][-(i*5)] < price_confirmation['Close'][-(i*5)]):
        #     return True
        # else:
        #     return False
    else:
        return False
        
        