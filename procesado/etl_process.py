import pandas as pd
import numpy as np
import datetime

import yfinance as yf

#calculation of exponential moving average
def EMA(df, n):
    EMA = pd.Series(df.ewm(span=n, min_periods=n).mean(), name='EMA_' + str(n))
    return EMA

#calculation of rate of change
def ROC(df, n):
    M = df.diff(n - 1)
    N = df.shift(n - 1)
    ROC = pd.Series(((M / N) * 100), name = 'ROC_' + str(n))
    return ROC

#Calculation of price momentum
def MOM(df, n):
    MOM = pd.Series(df.diff(n), name='Momentum_' + str(n))
    return MOM

#calculation of relative strength index
def RSI(series, period):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    #rs = pd.stats.moments.ewma(u, com=period-1, adjust=False)
    rs=pd.DataFrame.ewm(u,com=period-1,adjust=False).mean()
    pd.DataFrame.ewm(d,com=period-1,adjust=False).mean()
    #pd.stats.moments.ewma(d, com=period-1, adjust=False)
    return 100 - 100 / (1 + (rs))

#calculation of stochastic osillator.

def STOK(close, low, high, n):
    STOK = ((close - low.rolling(n).mean()) / (high.rolling(n).mean() - low.rolling(n).mean())) * 100
    return STOK

def STOD(close, low, high, n):
    STOK = ((close - low.rolling(n).mean()) / (high.rolling(n).mean() - low.rolling(n).mean())) * 100
    STOD = STOK.rolling(3).mean()
    return STOD

#Calculation of moving average
def MA(df, n):
    MA = pd.Series(df.rolling(n, min_periods=n).mean(), name='MA_' + str(n))
    return MA

media_mov_short = 7
media_mov_med = 25
media_mov_long = 99

#
#get data from Yahoo finance.
#
btcoin = yf.download("BTC-USD,ETH-USD,ADA-USD,XRP-USD,BNB-USD,USDT-USD,^VIX,^GSPC,GC=F,EURUSD=X",start="2015-01-01", end="2021-05-1")
#Transform
btcoin.reset_index(inplace = True)
btcoin['year'] = btcoin['Date'].map(lambda x: x.year)
btcoin['month'] = btcoin['Date'].map(lambda x: x.month)
btcoin['monthf'] = btcoin['Date'].dt.month_name()
btcoin['week'] = btcoin['Date'].map(lambda x: x.week)
btcoin['weekday'] = btcoin['Date'].map(lambda x: x.day)
btcoin['Weekdayf'] = btcoin['Date'].dt.day_name()
btcoin['EMA21'] = EMA(btcoin['Close']['BTC-USD'], media_mov_short)
btcoin['EMA63'] = EMA(btcoin['Close']['BTC-USD'], media_mov_med)
btcoin['EMA252'] = EMA(btcoin['Close']['BTC-USD'], media_mov_long)

btcoin['bollingerSMA_MVS'] = btcoin['Close']['BTC-USD'].rolling(window=media_mov_short).mean()
btcoin['bollingerSMA_MVM'] = btcoin['Close']['BTC-USD'].rolling(window=media_mov_med).mean()
btcoin['bollingerSMA_MVL'] = btcoin['Close']['BTC-USD'].rolling(window=media_mov_long).mean()
btcoin['bollingerSTD_MVS'] = btcoin['Close']['BTC-USD'].rolling(window=media_mov_short).std()
btcoin['bollingerSTD_MVM'] = btcoin['Close']['BTC-USD'].rolling(window=media_mov_med).std()
btcoin['bollingerSTD_MVL'] = btcoin['Close']['BTC-USD'].rolling(window=media_mov_long).std()
btcoin['Upper_MVS'] = btcoin['bollingerSMA_MVS'] + (btcoin['bollingerSTD_MVS'] * 2)
btcoin['Lower_MVS'] = btcoin['bollingerSMA_MVS'] - (btcoin['bollingerSTD_MVS'] * 2)
btcoin['Upper_MVM'] = btcoin['bollingerSMA_MVM'] + (btcoin['bollingerSTD_MVM'] * 2)
btcoin['Lower_MVM'] = btcoin['bollingerSMA_MVM'] - (btcoin['bollingerSTD_MVM'] * 2)
btcoin['Upper_MVL'] = btcoin['bollingerSMA_MVL'] + (btcoin['bollingerSTD_MVL'] * 2)
btcoin['Lower_MVL'] = btcoin['bollingerSMA_MVL'] - (btcoin['bollingerSTD_MVL'] * 2)


btcoin['MACD'] = btcoin['EMA21'] - btcoin['EMA63']

btcoin['ROC21'] = ROC(btcoin['Close']['BTC-USD'], media_mov_short)
btcoin['ROC63'] = ROC(btcoin['Close']['BTC-USD'], media_mov_med)

btcoin['MOM21'] = MOM(btcoin['Close']['BTC-USD'], media_mov_short)
btcoin['MOM63'] = MOM(btcoin['Close']['BTC-USD'], media_mov_med)

btcoin['RSI21'] = RSI(btcoin['Close']['BTC-USD'], media_mov_short)
btcoin['RSI63'] = RSI(btcoin['Close']['BTC-USD'], media_mov_med)
btcoin['RSI252'] = RSI(btcoin['Close']['BTC-USD'], media_mov_long)

btcoin['%K21'] = STOK(btcoin['Close']['BTC-USD'], btcoin['Low']['BTC-USD'], btcoin['High']['BTC-USD'], media_mov_short)
btcoin['%D21'] = STOD(btcoin['Close']['BTC-USD'], btcoin['Low']['BTC-USD'], btcoin['High']['BTC-USD'], media_mov_short)
btcoin['%K63'] = STOK(btcoin['Close']['BTC-USD'], btcoin['Low']['BTC-USD'], btcoin['High']['BTC-USD'], media_mov_med)
btcoin['%D63'] = STOD(btcoin['Close']['BTC-USD'], btcoin['Low']['BTC-USD'], btcoin['High']['BTC-USD'], media_mov_med)
btcoin['%K252'] = STOK(btcoin['Close']['BTC-USD'], btcoin['Low']['BTC-USD'], btcoin['High']['BTC-USD'], media_mov_long)
btcoin['%D252'] = STOD(btcoin['Close']['BTC-USD'], btcoin['Low']['BTC-USD'], btcoin['High']['BTC-USD'], media_mov_long)

btcoin['MA21'] = MA(btcoin['Close']['BTC-USD'], media_mov_short)
btcoin['MA63'] = MA(btcoin['Close']['BTC-USD'], media_mov_med)
btcoin['MA252'] = MA(btcoin['Close']['BTC-USD'], media_mov_long)

btcoin.dropna(inplace=True)

btcoin.corr()

btcoin.to_csv("bitcoin_dataset.csv")


