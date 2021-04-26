import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import yfinance as yf

#calculation of exponential moving average
def EMA(df, n):
    EMA = pd.Series(df['Close'].ewm(span=n, min_periods=n).mean(), name='EMA_' + str(n))
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
    rs=pd.DataFrame.ewm(u,com=period-1,adjust=False).mean()
    pd.DataFrame.ewm(d,com=period-1,adjust=False).mean()
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
    MA = pd.Series(df['Close'].rolling(n, min_periods=n).mean(), name='MA_' + str(n))
    return MA


def GDT():
    btcoin = yf.download("BTC-USD", start="2015-01-01", end="2021-04-23")
    btcoin.reset_index(inplace = True)
    btcoin.tail()
    media_mov_short = 7
    media_mov_med = 25
    media_mov_long = 99
    btcoin['signal'] = 0.0

    # Create short simple moving average over the short window
    btcoin['short_mavg'] = btcoin['Close'].rolling(window=media_mov_short, min_periods=1, center=False).mean()

    # Create long simple moving average over the long window
    btcoin['long_mavg'] = btcoin['Close'].rolling(window=media_mov_med, min_periods=1, center=False).mean()

    # Create signals
    btcoin['signal'] = np.where(btcoin['short_mavg'] > btcoin['long_mavg'], 1.0, 0.0)
    btcoin.tail()
    return btcoin
    
def PDG(btcoin):
    media_mov_short = 7
    media_mov_med = 25
    media_mov_long = 99
    btcoin['EMA21'] = EMA(btcoin, media_mov_short)
    btcoin['EMA63'] = EMA(btcoin, media_mov_med)
    btcoin['EMA252'] = EMA(btcoin, media_mov_long)
    btcoin['bollingerSMA_MVS'] = btcoin['Close'].rolling(window=media_mov_short).mean()
    btcoin['bollingerSMA_MVM'] = btcoin['Close'].rolling(window=media_mov_med).mean()
    btcoin['bollingerSMA_MVL'] = btcoin['Close'].rolling(window=media_mov_long).mean()
    btcoin['bollingerSTD_MVS'] = btcoin['Close'].rolling(window=media_mov_short).std()
    btcoin['bollingerSTD_MVM'] = btcoin['Close'].rolling(window=media_mov_med).std()
    btcoin['bollingerSTD_MVL'] = btcoin['Close'].rolling(window=media_mov_long).std()
    btcoin['Upper_MVS'] = btcoin['bollingerSMA_MVS'] + (btcoin['bollingerSTD_MVS'] * 2)
    btcoin['Lower_MVS'] = btcoin['bollingerSMA_MVS'] - (btcoin['bollingerSTD_MVS'] * 2)
    btcoin['Upper_MVM'] = btcoin['bollingerSMA_MVM'] + (btcoin['bollingerSTD_MVM'] * 2)
    btcoin['Lower_MVM'] = btcoin['bollingerSMA_MVM'] - (btcoin['bollingerSTD_MVM'] * 2)
    btcoin['Upper_MVL'] = btcoin['bollingerSMA_MVL'] + (btcoin['bollingerSTD_MVL'] * 2)
    btcoin['Lower_MVL'] = btcoin['bollingerSMA_MVL'] - (btcoin['bollingerSTD_MVL'] * 2)
    btcoin['MACD'] = btcoin['EMA21'] - btcoin['EMA63']
    btcoin['ROC21'] = ROC(btcoin['Close'], media_mov_short)
    btcoin['ROC63'] = ROC(btcoin['Close'], media_mov_med)
    btcoin['MOM21'] = MOM(btcoin['Close'], media_mov_short)
    btcoin['MOM63'] = MOM(btcoin['Close'], media_mov_med)
    btcoin['RSI21'] = RSI(btcoin['Close'], media_mov_short)
    btcoin['RSI63'] = RSI(btcoin['Close'], media_mov_med)
    btcoin['RSI252'] = RSI(btcoin['Close'], media_mov_long)
    btcoin['%K21'] = STOK(btcoin['Close'], btcoin['Low'], btcoin['High'], media_mov_short)
    btcoin['%D21'] = STOD(btcoin['Close'], btcoin['Low'], btcoin['High'], media_mov_short)
    btcoin['%K63'] = STOK(btcoin['Close'], btcoin['Low'], btcoin['High'], media_mov_med)
    btcoin['%D63'] = STOD(btcoin['Close'], btcoin['Low'], btcoin['High'], media_mov_med)
    btcoin['%K252'] = STOK(btcoin['Close'], btcoin['Low'], btcoin['High'], media_mov_long)
    btcoin['%D252'] = STOD(btcoin['Close'], btcoin['Low'], btcoin['High'], media_mov_long)
    btcoin['MA21'] = MA(btcoin, media_mov_short)
    btcoin['MA63'] = MA(btcoin, media_mov_med)
    btcoin['MA252'] = MA(btcoin, media_mov_long)
    btcoin.dropna(inplace=True)
    return btcoin
    
def TDG(actual,anter,vp_1d,vp_5d,vp_30d):
    
    if actual > anter:
        max_val_act = actual
        diff_act = actual - anter
        diff_act = (diff_act/max_val_act)*100
    else:
        max_val_act = anter
        diff_act = anter - actual
        diff_act = -(diff_act/max_val_act)*100
    
    if actual > vp_1d:
        max_val_1d = actual
        diff_1d = actual - vp_1d
        diff_p1d = -(diff_1d/max_val_1d)*100
    else:
        max_val_1d = vp_1d
        diff_1d = vp_1d - actual
        diff_p1d = (diff_1d/max_val_1d)*100
        
    if actual > vp_5d:
        max_val_5d = actual
        diff_5d = actual - vp_5d
        diff_p5d = -(diff_5d/max_val_5d)*100
    else:
        max_val_5d = vp_5d
        diff_5d = vp_5d - actual
        diff_p5d = (diff_5d/max_val_5d)*100
        
    if actual > vp_30d:
        max_val_30d = actual
        diff_30d = actual - vp_30d
        diff_p30d = -(diff_30d/max_val_30d)*100
    else:
        max_val_30d = vp_30d
        diff_30d = vp_30d - actual
        diff_p30d = (diff_30d/max_val_30d)*100
    
    data = {'':['actual','1d','5d','30d'],'Valor':[actual,vp_1d,vp_5d,vp_30d],'Diferencial':[diff_act,diff_p1d,diff_p5d,diff_p30d]}
    pd_data=pd.DataFrame(data)
    pd_data = pd_data.round(2)
    return pd_data

def main():
    data_raw = GDT()
    data = PDG(data_raw)
    prediction =TDG(round(data['Close'].iloc[-1],3),49523.3,52343.00,54000.2,48001.23)
    col1, col2, col3 = st.beta_columns([1,3,1])
    col2.image('image/kiribati-logo.png', width=424)
    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == 'Home':
        st.subheader("Bitcoin price")
        st.line_chart(data['EMA63'])
        col1, col2, col3 = st.beta_columns([1,3,1])
        col2.write('Tabla de previsiones:')
        col2.write(prediction)
        
    else:
        st.subheader("About")
        st.write('Hola Amig@, somos Kiribati. En que podemos ayudarte?')
        field_1 = st.text_input('¿Cual es tu nombre?')
        field_2 = st.text_input('¿cual es tu e-mail?')
        field_3 = st.text_area('Por favor, dinos en que podemos ayudarte')
        if st.button('Enviar'):
            st.write('Te contestaremos lo antes posible, Gracias!')

if __name__=='__main__':
    main()
