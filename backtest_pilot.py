#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 18:16:34 2022

@author: pranav.atulya
"""

from utils.getData import getOHLC
from getIndicators import *
from OLS import OLS_max, regression_channel
import statistics
from strategies.strat1 import strat1

stock = 'AAPL'
interval_primary = '15m'
interval_confirmation = '1m'
period = '1mo'

price_primary = getOHLC(stock, period, interval_primary)
price_primary = price_primary.drop(columns = ['High', 'Low', 'Volume'], axis = 1)

price_primary = getBollingerBands(price_primary)
price_primary = getMACD(price_primary)
price_primary['SMA50'] = price_primary['Close'].rolling(window = 50).mean()

# Don't use price_primary here, create a new dataframe for regression
price_predict = regression_channel(price_primary)

price_primary['MACD_mean'] = price_primary['signal_line'].mean()
price_primary['MACD_dev'] = price_primary['signal_line'].std()
########################################################################################################################
# price_confirmation = getOHLC(stock, period, interval_confirmation)

# price_confirmation = getBollingerBands(price_confirmation)
# price_confirmation = getMACD(price_confirmation)
# price_confirmation = getSMA(price_confirmation)
# price_confirmation = regression_channel(price_confirmation)
########################################################################################################################

balance = 10000
price_primary['Signal'] = 'No Position'

target = 2
stoploss = -1.5


price_primary['Sys_B'] = balance
price_primary['PeriodPnL'] = ((price_primary['Open']/price_primary['Open'].shift(1))-1)*100
price_primary['TradePnL'] = 0

for i in range(1,len(price_primary)):
    MyPnL = 0
    condition1 = price_primary['SMA50'][i] > price_primary['Close'][i]#strat1(price_primary, price_confirmation, i)    
    if(condition1):     
        while(price_primary['TradePnL'][i] < target and price_primary['TradePnL'][i] > stoploss and i in range(i,len(price_primary)-1)):
            
            price_primary.iloc[i, price_primary.columns.get_loc('Signal')] = "BUY"
            price_primary.iloc[i+1, price_primary.columns.get_loc('TradePnL')] = ((1 + (price_primary['TradePnL'][i]/100)) * (1 + (price_primary['PeriodPnL'][i+1]/100)) - 1) * 100
            if(price_primary['TradePnL'][i+1]>=target or price_primary['TradePnL'][i+1]<=stoploss):
                price_primary.iloc[i+1:len(price_primary)-1 , price_primary.columns.get_loc('Sys_B')] = price_primary['Sys_B'][i] + price_primary['Sys_B'][i+1]*(price_primary['TradePnL'][i+1]/100)  
            
            i += 1
            
    else:
        pass

winners = price_primary[price_primary['TradePnL']>=target]
losers = price_primary[price_primary['TradePnL']<=stoploss]  
duration = price_primary[price_primary['TradePnL']!= 0]     

  
      

avg_gain = price_primary['Sys_B'][-2]



print("Average Portfolio value ", avg_gain)    
print("Total trades taken ", len(winners) + len(losers) )
print("Total winners ", len(winners))
print("Holding period per trade ", len(duration)/(len(winners)+len(losers)))
print("Win Ratio ", len(winners)/(len(winners) + len(losers)))
# print("Average win ratio", statistics.mean(tot_winners_list)/statistics.mean(tot_trades_list))
# price.to_csv("BTCnewBT.csv")


