import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import calmap

def read_data_csv():
    df = pd.read_csv("../data/data_visualization.csv",sep=',')
    return df

def plot_candles(data):

    return fig
    
def main():
    datavi = read_data_csv()
    col1, col2, col3 = st.beta_columns([1,3,1])
    col2.image('image/kiribati-logo.png', width=424)
    col1, col2 = st.beta_columns((5,1))
    fig = go.Figure(data=[go.Candlestick(x=datavi['Date'],open=datavi['BT_Open'], high=datavi['BT_High'],low=datavi['BT_Low'], close=datavi['BT_Close'],name="Bitcoin")])
    fig.add_trace(go.Scatter(
        x=datavi['Date'],
        y=datavi['ma_short'],
        name="MA 5 days"       # this sets its legend entry
    ))
    fig.add_trace(go.Scatter(
        x=datavi['Date'],
        y=datavi['ma_medium'],
        name="MA 25 days"       # this sets its legend entry
    ))
    fig.update_layout(height=600, width=600, title_text="Bitcoin value evolution", xaxis_rangeslider_visible=False)
    col1.plotly_chart(fig)
    
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
    col2.plotly_chart(fig1)
    
    col3, col4 = st.beta_columns(2)
    objects = ('Bitcoin', 'Ethereum', 'Cardano', 'Ripple', 'Binance', 'Tether')
    y_pos = np.arange(len(objects))
    performance = [datavi['BT_Volume'].iloc[-1],datavi['ETH_Volume'].iloc[-1],datavi['ADA_Volume'].iloc[-1],datavi['XRP_Volume'].iloc[-1],datavi['BNB_Volume'].iloc[-1],datavi['USDT_Volume'].iloc[-1]]
    fig2, (ax) = plt.subplots()
    ax.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Coin Volume')
    plt.title('Cryptocoins volume market')
    col4.pyplot(fig2)


if __name__=='__main__':
    main()
