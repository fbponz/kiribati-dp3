import pandas as pd
import numpy as np
import datetime
import yfinance as yf

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
GSPCRAW = yf.download("^GSPC",start="2015-01-01", end="2021-05-1")
GCFRAW = yf.download("GC=F",start="2015-01-01", end="2021-05-1")

BTRAW.reset_index(inplace = True)
ETHRAW.reset_index(inplace = True)
ADARAW.reset_index(inplace = True)
XRPRAW.reset_index(inplace = True)
BNBRAW.reset_index(inplace = True)
USDTRAW.reset_index(inplace = True)
GSPCRAW.reset_index(inplace = True)
GCFRAW.reset_index(inplace = True)

BTRAW = BTRAW.add_prefix('BT_')
ETHRAW = ETHRAW.add_prefix('ETH_')
ADARAW = ADARAW.add_prefix('ADA_')
XRPRAW = XRPRAW.add_prefix('XRP_')
BNBRAW = BNBRAW.add_prefix('BNB_')
USDTRAW = USDTRAW.add_prefix('USDT_')
GSPCRAW = GSPCRAW.add_prefix('GSPC_')
GCFRAW = GCFRAW.add_prefix('GCF_')

Dataset = pd.merge(left=BTRAW, right=ETHRAW, how='left', left_on='BT_Date', right_on='ETH_Date')
Dataset = pd.merge(left=Dataset, right=ADARAW, how='left', left_on='BT_Date', right_on='ADA_Date')
Dataset = pd.merge(left=Dataset, right=XRPRAW, how='left', left_on='BT_Date', right_on='XRP_Date')
Dataset = pd.merge(left=Dataset, right=BNBRAW, how='left', left_on='BT_Date', right_on='BNB_Date')
Dataset = pd.merge(left=Dataset, right=USDTRAW, how='left', left_on='BT_Date', right_on='USDT_Date')
Dataset = pd.merge(left=Dataset, right=GSPCRAW, how='left', left_on='BT_Date', right_on='GSPC_Date')
Dataset = pd.merge(left=Dataset, right=GCFRAW, how='left', left_on='BT_Date', right_on='GCF_Date')
Dataset.drop(['ETH_Date', 'ADA_Date', 'XRP_Date', 'BNB_Date', 'USDT_Date',  'GSPC_Date', 'GCF_Date'], axis=1, inplace=True)
Dataset.rename(columns={"BT_Date":"Date"},inplace=True)

#Transform

Dataset['year'] = Dataset['Date'].map(lambda x: x.year)
Dataset['month'] = Dataset['Date'].map(lambda x: x.month)
Dataset['monthf'] = Dataset['Date'].dt.month_name()
Dataset['week'] = Dataset['Date'].map(lambda x: x.week)
Dataset['weekday'] = Dataset['Date'].map(lambda x: x.day)
Dataset['weekdayf'] = Dataset['Date'].dt.day_name()


Dataset['MA21'] = MA(Dataset['BT_Close'], media_mov_short)
Dataset['MA63'] = MA(Dataset['BT_Close'], media_mov_med)
Dataset['MA252'] = MA(Dataset['BT_Close'], media_mov_long)

Dataset.dropna(inplace=True)

##Datos visualization

Dataset_visualization = pd.concat([Dataset['Date'],Dataset['year'],Dataset['month'],Dataset['monthf'],Dataset['week'],Dataset['weekday'],Dataset['weekdayf'],Dataset['MA21'],Dataset['MA63'],Dataset['MA252'],Dataset['BT_Close'],Dataset['BT_Open'],Dataset['BT_High'],Dataset['BT_Low'],Dataset['BT_Volume'],Dataset['ETH_Close'],Dataset['ETH_Volume'],Dataset['ADA_Close'],Dataset['ADA_Volume'],Dataset['XRP_Close'],Dataset['XRP_Volume'],Dataset['BNB_Close'],Dataset['BNB_Volume'],Dataset['USDT_Close'],Dataset['USDT_Volume']], axis=1, keys=['Date','year','month','monthf','week','weekday','weekdayf','ma_short','ma_medium','ma_long','BT_Close','BT_Open','BT_High','BT_Low','BT_Volume','ETH_Close','ETH_Volume','ADA_Close','ADA_Volume','XRP_Close','XRP_Volume','BNB_Close','BNB_Volume','USDT_Close','USDT_Volume'])

##Slice a concrete months

Dataset_visualization.to_csv("../data/data_visualization.csv")
print("Data Visualization file created")
