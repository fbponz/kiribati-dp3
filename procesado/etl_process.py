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
BTRAW = yf.download("BTC-USD",start="2015-01-01", end="2021-05-1")
ETHRAW = yf.download("ETH-USD",start="2015-01-01", end="2021-05-1")
ADARAW = yf.download("ADA-USD",start="2015-01-01", end="2021-05-1")
XRPRAW = yf.download("XRP-USD",start="2015-01-01", end="2021-05-1")
BNBRAW = yf.download("BNB-USD",start="2015-01-01", end="2021-05-1")
USDTRAW = yf.download("USDT-USD",start="2015-01-01", end="2021-05-1")
VIXRAW = yf.download("^VIX",start="2015-01-01", end="2021-05-1")
GSPCRAW = yf.download("^GSPC",start="2015-01-01", end="2021-05-1")
GCFRAW = yf.download("GC=F",start="2015-01-01", end="2021-05-1")
EURUSDCHANRAW = yf.download("EURUSD=X",start="2015-01-01", end="2021-05-1")

BTRAW.reset_index(inplace = True)
ETHRAW.reset_index(inplace = True)
ADARAW.reset_index(inplace = True)
XRPRAW.reset_index(inplace = True)
BNBRAW.reset_index(inplace = True)
USDTRAW.reset_index(inplace = True)
VIXRAW.reset_index(inplace = True)
GSPCRAW.reset_index(inplace = True)
GCFRAW.reset_index(inplace = True)
EURUSDCHANRAW.reset_index(inplace = True)

BTRAW = BTRAW.add_prefix('BT_')
ETHRAW = ETHRAW.add_prefix('ETH_')
ADARAW = ADARAW.add_prefix('ADA_')
XRPRAW = XRPRAW.add_prefix('XRP_')
BNBRAW = BNBRAW.add_prefix('BNB_')
USDTRAW = USDTRAW.add_prefix('USDT_')
VIXRAW = VIXRAW.add_prefix('VIX_')
GSPCRAW = GSPCRAW.add_prefix('GSPC_')
GCFRAW = GCFRAW.add_prefix('GCF_')
EURUSDCHANRAW = EURUSDCHANRAW.add_prefix('EURUSDCHAN_')

Dataset = pd.merge(left=BTRAW, right=ETHRAW, how='left', left_on='BT_Date', right_on='ETH_Date')
Dataset = pd.merge(left=Dataset, right=ADARAW, how='left', left_on='BT_Date', right_on='ADA_Date')
Dataset = pd.merge(left=Dataset, right=XRPRAW, how='left', left_on='BT_Date', right_on='XRP_Date')
Dataset = pd.merge(left=Dataset, right=BNBRAW, how='left', left_on='BT_Date', right_on='BNB_Date')
Dataset = pd.merge(left=Dataset, right=USDTRAW, how='left', left_on='BT_Date', right_on='USDT_Date')
Dataset = pd.merge(left=Dataset, right=VIXRAW, how='left', left_on='BT_Date', right_on='VIX_Date')
Dataset = pd.merge(left=Dataset, right=GSPCRAW, how='left', left_on='BT_Date', right_on='GSPC_Date')
Dataset = pd.merge(left=Dataset, right=GCFRAW, how='left', left_on='BT_Date', right_on='GCF_Date')
Dataset = pd.merge(left=Dataset, right=EURUSDCHANRAW, how='left', left_on='BT_Date', right_on='EURUSDCHAN_Date')
Dataset.drop(['ETH_Date', 'ADA_Date', 'XRP_Date', 'BNB_Date', 'USDT_Date', 'VIX_Date', 'GSPC_Date', 'GCF_Date', 'EURUSDCHAN_Date'], axis=1, inplace=True)
Dataset.rename(columns={"BT_Date":"Date"},inplace=True)

#Transform

Dataset['year'] = Dataset['Date'].map(lambda x: x.year)
Dataset['month'] = Dataset['Date'].map(lambda x: x.month)
Dataset['monthf'] = Dataset['Date'].dt.month_name()
Dataset['week'] = Dataset['Date'].map(lambda x: x.week)
Dataset['weekday'] = Dataset['Date'].map(lambda x: x.day)
Dataset['weekdayf'] = Dataset['Date'].dt.day_name()
Dataset['EMA21'] = EMA(Dataset['BT_Close'], media_mov_short)
Dataset['EMA63'] = EMA(Dataset['BT_Close'], media_mov_med)
Dataset['EMA252'] = EMA(Dataset['BT_Close'], media_mov_long)

Dataset['bollingerSMA_MVS'] = Dataset['BT_Close'].rolling(window=media_mov_short).mean()
Dataset['bollingerSMA_MVM'] = Dataset['BT_Close'].rolling(window=media_mov_med).mean()
Dataset['bollingerSMA_MVL'] = Dataset['BT_Close'].rolling(window=media_mov_long).mean()
Dataset['bollingerSTD_MVS'] = Dataset['BT_Close'].rolling(window=media_mov_short).std()
Dataset['bollingerSTD_MVM'] = Dataset['BT_Close'].rolling(window=media_mov_med).std()
Dataset['bollingerSTD_MVL'] = Dataset['BT_Close'].rolling(window=media_mov_long).std()
Dataset['Upper_MVS'] = Dataset['bollingerSMA_MVS'] + (Dataset['bollingerSTD_MVS'] * 2)
Dataset['Lower_MVS'] = Dataset['bollingerSMA_MVS'] - (Dataset['bollingerSTD_MVS'] * 2)
Dataset['Upper_MVM'] = Dataset['bollingerSMA_MVM'] + (Dataset['bollingerSTD_MVM'] * 2)
Dataset['Lower_MVM'] = Dataset['bollingerSMA_MVM'] - (Dataset['bollingerSTD_MVM'] * 2)
Dataset['Upper_MVL'] = Dataset['bollingerSMA_MVL'] + (Dataset['bollingerSTD_MVL'] * 2)
Dataset['Lower_MVL'] = Dataset['bollingerSMA_MVL'] - (Dataset['bollingerSTD_MVL'] * 2)


Dataset['MACD'] = Dataset['EMA21'] - Dataset['EMA63']

Dataset['ROC21'] = ROC(Dataset['BT_Close'], media_mov_short)
Dataset['ROC63'] = ROC(Dataset['BT_Close'], media_mov_med)

Dataset['MOM21'] = MOM(Dataset['BT_Close'], media_mov_short)
Dataset['MOM63'] = MOM(Dataset['BT_Close'], media_mov_med)

Dataset['RSI21'] = RSI(Dataset['BT_Close'], media_mov_short)
Dataset['RSI63'] = RSI(Dataset['BT_Close'], media_mov_med)
Dataset['RSI252'] = RSI(Dataset['BT_Close'], media_mov_long)

Dataset['%K21'] = STOK(Dataset['BT_Close'], Dataset['BT_Low'], Dataset['BT_High'], media_mov_short)
Dataset['%D21'] = STOD(Dataset['BT_Close'], Dataset['BT_Low'], Dataset['BT_High'], media_mov_short)
Dataset['%K63'] = STOK(Dataset['BT_Close'], Dataset['BT_Low'], Dataset['BT_High'], media_mov_med)
Dataset['%D63'] = STOD(Dataset['BT_Close'], Dataset['BT_Low'], Dataset['BT_High'], media_mov_med)
Dataset['%K252'] = STOK(Dataset['BT_Close'], Dataset['BT_Low'], Dataset['BT_High'], media_mov_long)
Dataset['%D252'] = STOD(Dataset['BT_Close'], Dataset['BT_Low'], Dataset['BT_High'], media_mov_long)

Dataset['MA21'] = MA(Dataset['BT_Close'], media_mov_short)
Dataset['MA63'] = MA(Dataset['BT_Close'], media_mov_med)
Dataset['MA252'] = MA(Dataset['BT_Close'], media_mov_long)

Dataset.dropna(inplace=True)

Dataset.corr()

Dataset.to_csv("../data/data_raw.csv")
print("Data Raw file created")

##Datos visualization

Dataset_visualization = pd.concat([Dataset['Date'],Dataset['year'],Dataset['month'],Dataset['monthf'],Dataset['week'],Dataset['weekday'],Dataset['weekdayf'],Dataset['MA21'],Dataset['MA63'],Dataset['MA252'],Dataset['BT_Close'],Dataset['BT_Open'],Dataset['BT_High'],Dataset['BT_Low'],Dataset['BT_Volume'],Dataset['ETH_Close'],Dataset['ETH_Volume'],Dataset['ADA_Close'],Dataset['ADA_Volume'],Dataset['XRP_Close'],Dataset['XRP_Volume'],Dataset['BNB_Close'],Dataset['BNB_Volume'],Dataset['USDT_Close'],Dataset['USDT_Volume']], axis=1, keys=['Date','year','month','monthf','week','weekday','weekdayf','ma_short','ma_medium','ma_long','BT_Close','BT_Open','BT_High','BT_Low','BT_Volume','ETH_Close','ETH_Volume','ADA_Close','ADA_Volume','XRP_Close','XRP_Volume','BNB_Close','BNB_Volume','USDT_Close','USDT_Volume'])

##Slice a concrete months
Dataset_visualization = Dataset_visualization[Dataset_visualization["year"]==2021]
Dataset_visualization = Dataset_visualization[Dataset_visualization["month"]>0]
Dataset_visualization.to_csv("../data/data_visualization.csv")
print("Data Visualization file created")
