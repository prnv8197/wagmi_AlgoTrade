#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 12:56:42 2021

@author: pranav.atulya
"""

import numpy as np

def getstoch_oscill(price, period = 14):
    price['%K'] = 0
    for i in len(price):
        if(i>14):
            lowest = min(price['Close'][i-period:i])
            highest = max(price['Close'][i-period:i])
            price['%K'][i] = ((price['Close'][i] - lowest)/(highest - lowest)) * 100
            return price

def getMACD(price, slow = 26, fast = 12, signal = 9):
    price['macd_line'] = price['Close'].ewm(span = fast).mean() - price['Close'].ewm(span = slow).mean()
    price['signal_line'] = price['macd_line'].ewm(span = signal).mean()
    price['macd_diff'] = price['macd_line'] - price['signal_line']
    return price

def getRSI(price, period = 14):
    price['upmove'] = 0
    price['downmove'] = 0
    for i in range(len(price['Close'])):
        # if(price['Close'][i]>price['Close'][i-1]):
        price['upmove'] = np.where(price['Close'] > price['Close'].shift(1), price['Close'] - price['Close'].shift(1), 0)
        # else:
        price['downmove'] = np.where(price['Close'] < price['Close'].shift(1), price['Close'].shift(1) - price['Close'], 0)
        
    price['Avg_upmove'] = price['upmove'].rolling(window = period).mean()
    price['Avg_downmove'] = price['downmove'].rolling(window = period).mean()
    price['RS'] = price['Avg_upmove']/price['Avg_downmove']
    price['RSI'] = 100 - (100/(1+price['RS']))
    price = price.drop(columns = ['Avg_upmove', 'Avg_downmove', 'RS'], axis=1)
    return price     

def getBollingerBands(price):
    price['MA']=price['Close'].rolling(window=20).mean()
    price['StdDev']=price['Close'].rolling(window=20).std() 
    price['Upper Band'] = price['MA'] + (price['StdDev'] * 2)
    price['Lower Band'] = price['MA'] - (price['StdDev'] * 2)
    return price    

def getDEMA(price, timeFrame = 50):    
        ema = price['Close'].ewm(span = timeFrame, adjust = False).mean()
        dema = 2 * ema - ema.ewm(span = timeFrame, adjust = False).mean()
        return dema

def getatr(price, period = 14):
    price['H-L'] = price['High']-price['Low']
    price['H-pC'] = abs(price['High']-price['Close'].shift(1))
    price['L-pC'] = abs(price['Low']-price['Close'].shift(1))
    price['TR'] = price[['H-L', 'H-pC', 'L-pC']].max(axis = 1)
    price['ATR'] = price['TR'].rolling(window = period).mean()
    price = price.drop(['H-L', 'H-pC', 'L-pC', 'TR'], axis = 1)
    return price     