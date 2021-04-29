import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import mpl_finance as mpf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

def read_data_csv():
    df = pd.read_csv("../data/data_prediction.csv",sep=';')
    return df
    
def main():
    data = read_data_csv()
    col1, col2, col3 = st.beta_columns([1,3,1])
    col2.image('image/kiribati-logo.png', width=424)
    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == 'Home':
        st.subheader("Bitcoin price")
        fig = plt.figure(figsize=(24, 8))
        ax = fig.add_subplot(1, 1, 1)
        mpf.candlestick2_ochl(ax, data['Open'], data['Close'], data['High'],
                data['Low'], width=0.6, colorup='g', colordown='r', alpha=0.75)
        st.pyplot(fig)
        
        col1, col2, col3 = st.beta_columns([1,6,1])
        col2.write('Tabla de previsiones:')
        col2.write(data)
        
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
