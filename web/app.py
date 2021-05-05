import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import date
import seaborn as sns
import calmap

def read_data_csv():
    df = pd.read_csv("../data/data_visualization.csv",sep=',')
    df = df[df["year"]==2021]
    df = df[df["month"]>2]
    return df

def read_data_prediction():
    df = pd.read_csv("../data/data_prediccion_30d.csv",sep=',')
    df = df[df["year"]==2021]
    df = df[df["month"]>2]
    return df

def read_data_bitcoin():
    df = read_data_prediction()
    #data = [df.loc[[-31], ['BT_Close']], df.loc[[-30], ['BT_Close']], df.loc[[-5], ['BT_Close']], df.loc[[-1], ['BT_Close']]]
    return df
def transform_data_bitcoin(data_in):
    data = [0, 0.9, 3.6, 10]
    return data
    
def main():
    datavi = read_data_csv()
    datapredict = read_data_prediction()
    st.set_page_config(layout="wide")
    col1, col2, col3 = st.beta_columns([6,6,6])
    col2.image('image/kiribati-logo.png', width=424)
    col1, col2 = st.beta_columns((1,1))
    fig = go.Figure(data=[go.Candlestick(x=datavi['Date'],open=datavi['BT_Open'], high=datavi['BT_High'],low=datavi['BT_Low'], close=datavi['BT_Close'],name="Bitcoin")])
    fig.add_trace(go.Scatter(
        x=datavi['Date'],
        y=datavi['ma_short'],
        name="MA 5 days",       # this sets its legend entry
        line_color='rgb(0,176,246)'
    ))
    fig.add_trace(go.Scatter(
        x=datavi['Date'],
        y=datavi['ma_medium'],
        name="MA 25 days",       # this sets its legend entry
        line_color='rgb(255,0,255)'
    ))
    fig.add_trace(go.Scatter(
        x=datapredict['Date'],
        y=datapredict['Forecast_ARIMAX'],
        name="Predicted BT_Close",       # this sets its legend entry
        line_color='rgb(10,10,10)'
    ))
    fig.update_layout(height=600, width=600, title_text="Bitcoin value evolution", xaxis_rangeslider_visible=False)
    col1.plotly_chart(fig)
    
    
    
    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    datapredict = read_data_bitcoin()
    
    fig3 = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>Time</b>','<b>Value</b>'],
    line_color='darkslategray',
    fill_color=headerColor,
    align=['left','center'],
    font=dict(color='white', size=14)
      ),
      cells=dict(
        values=[
           datapredict["Date"],
           datapredict["BT_Close"]],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
        align = ['left', 'center'],
        font = dict(color = 'darkslategray', size = 14)
        ))
    ])
    
    fig3.update_layout(height=600, width=600, title_text="Bitcoin value evolution", xaxis_rangeslider_visible=False)
    col2.plotly_chart(fig3)
    
    col3, col4 = st.beta_columns((1,1))
    fig1 = make_subplots(rows=5, cols=1)
    fig1.append_trace(go.Scatter(
        x=datavi['Date'],
        y=datavi['ETH_Close'],
        name="Ethereum"
    ), row=1, col=1)

    fig1.append_trace(go.Scatter(
        x=datavi['Date'],
        y=datavi['ADA_Close'],
        name="Cardano"
    ), row=2, col=1)
    
    fig1.append_trace(go.Scatter(
        x=datavi['Date'],
        y=datavi['XRP_Close'],
        name="Ripple"
    ), row=3, col=1)
    
    fig1.append_trace(go.Scatter(
        x=datavi['Date'],
        y=datavi['BNB_Close'],
        name="BNB"
    ), row=4, col=1)
    
    fig1.append_trace(go.Scatter(
        x=datavi['Date'],
        y=datavi['USDT_Close'],
        name="Tether"
    ), row=5, col=1)

    fig1.update_layout(height=600, width=600, title_text="Other Crypto-coins")
    col3.plotly_chart(fig1)
    
    performance = [datavi['BT_Volume'].iloc[-1],datavi['ETH_Volume'].iloc[-1],datavi['ADA_Volume'].iloc[-1],datavi['XRP_Volume'].iloc[-1],datavi['BNB_Volume'].iloc[-1],datavi['USDT_Volume'].iloc[-1]]
    fig2 = go.Figure(go.Bar(
                x=performance,
                y= ['Bitcoin', 'Ethereum', 'Cardano', 'Ripple', 'Binance', 'Tether-USD'],
                orientation='h'))
    fig2.update_layout(height=600, width=600, title_text="Market volume")

    col4.plotly_chart(fig2)


if __name__=='__main__':
    main()
