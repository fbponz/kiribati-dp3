import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def read_data_csv():
    df = pd.read_csv("../data/data_visualization.csv",sep=',')
    return df

def plot_candles(data):

    return fig
    
def main():
    datavi = read_data_csv()
    col1, col2, col3 = st.beta_columns([1,3,1])
    col2.image('image/kiribati-logo.png', width=424)
    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == 'Home':
        st.subheader("Home")
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
        fig.add_trace(go.Scatter(
            x=datavi['Date'],
            y=datavi['ma_long'],
            name="MA 100 days"       # this sets its legend entry
        ))
        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)
        
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
        st.plotly_chart(fig1)
        

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
