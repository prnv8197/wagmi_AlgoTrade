#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 19:17:17 2022

@author: pranav.atulya
"""

import pandas as pd
from getIndicators import *
from getData import getOHLC
import statistics
from OLS import OLS_max, regression_channel







stock = "BTC-USD"
interval = '5m'
period = '1mo'

price = getOHLC('BTC-USD', period = '1mo', interval = '15m')

balance = 10000
price['Signal'] = 'No Position'


target = 1.5
stoploss = -1


price = getBollingerBands(price)
price['50SMA'] = price['Close'].rolling(window = 50).mean()
price = getBollingerBands(price)
price = getMACD(price)

price_s = getOHLC('BTC-USD', period = '1mo', interval = '5m')
        
price['Sys_B'] = balance
price['PeriodPnL'] = ((price['Open']/price['Open'].shift(1))-1)*100
price['TradePnL'] = 0
print(price.head())
for i in range(1,len(price)):
    MyPnL = 0
    condition1 = price['50SMA'][-1] > price['Upper Band'][-1] and price['signal_line'][-1] < macd_mean-1*macd_dev 
    
    
    if(condition1):
        
        while(price['TradePnL'][i] < target and price['TradePnL'][i] > stoploss and i in range(i,len(price)-1)):
            
            price.iloc[i, price.columns.get_loc('Signal')] = "BUY"
            price.iloc[i+1, price.columns.get_loc('TradePnL')] = ((1 + (price['TradePnL'][i]/100)) * (1 + (price['PeriodPnL'][i+1]/100)) - 1) * 100
            if(price['TradePnL'][i+1]>=target or price['TradePnL'][i+1]<=stoploss):
                price.iloc[i+1:len(price)-1 , price.columns.get_loc('Sys_B')] = price['Sys_B'][i] + price['Sys_B'][i+1]*(price['TradePnL'][i+1]/100)  
            
            i += 1
            
    else:
        pass

winners = price[price['TradePnL']>=target]
losers = price[price['TradePnL']<=stoploss]  
duration = price[price['TradePnL']!= 0]     

  
      

avg_gain = price['Sys_B'][-2]


price.to_csv("BTCbt4.csv")
print("Average Portfolio value ", avg_gain)    
print("Total trades taken ", len(winners) + len(losers) )
print("Total winners ", len(winners))
print("Holding period per trade ", len(duration)/(len(winners)+len(losers)))
print("Win Ratio ", len(winners)/(len(winners) + len(losers)))
# print("Average win ratio", statistics.mean(tot_winners_list)/statistics.mean(tot_trades_list))
