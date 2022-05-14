#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 20:35:06 2022

@author: pranav.atulya
"""


import pandas as pd
from getIndicators import *

from getData import getOHLC
import statistics







stock = "AAPL"
# start = dt.datetime(2019, 8, 11) #yyyy/mm/dd
# end = dt.datetime(2019, 11, 11)
 
# price = pdr.get_data_yahoo(stock, start, end)
interval = '15m'
period = '1mo'

price = getOHLC(stock, period, interval)
price = price.drop(columns = ['High', 'Low', 'Volume'], axis = 1)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

balance = 10000
price['Signal'] = 'No Position'


target = 2
stoploss = -1.5

price = getBollingerBands(price)
price['50SMA'] = price['Close'].rolling(window = 50).mean()
price['Sys_B'] = balance
price['PeriodPnL'] = ((price['Open']/price['Open'].shift(1))-1)*100
price['TradePnL'] = 0

for i in range(1,len(price)):
    MyPnL = 0
    condition1 = price['50SMA'][i] > price['Close'][i]#price['Upper Band'][i] < price['50SMA'][i] and price['MA'][i] < price['Close'][i]
    
    
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



print("Average Portfolio value ", avg_gain)    
print("Total trades taken ", len(winners) + len(losers) )
print("Total winners ", len(winners))
print("Holding period per trade ", len(duration)/(len(winners)+len(losers)))
print("Win Ratio ", len(winners)/(len(winners) + len(losers)))
# print("Average win ratio", statistics.mean(tot_winners_list)/statistics.mean(tot_trades_list))
# price.to_csv("BTCnewBT.csv")