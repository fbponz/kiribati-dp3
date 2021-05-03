import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pmdarima import auto_arima
from sklearn.metrics import mean_absolute_error, mean_squared_error

myfavouritenumber = 13
seed = myfavouritenumber
np.random.seed(seed)

df = pd.read_csv("../data/data_filtered.csv")
df.set_index("Date", drop=False, inplace=True)
df.head()

df.drop(['monthf','Weekdayf'], axis=1)

df_train = df[df.year  < 2020]
df_valid = df[df.year >= 2020]

exogenous_features = ["BT_Open","BT_High","BT_Low","BT_Adj Close","BT_Volume","ETH_Open","ETH_High","ETH_Low","ETH_Close","ETH_Adj Close","ETH_Volume","ADA_Open","ADA_High","ADA_Low","ADA_Close","ADA_Adj Close","ADA_Volume","XRP_Volume","BNB_Open","BNB_High","BNB_Low","BNB_Close","BNB_Adj Close","BNB_Volume","USDT_Volume","VIX_Volume","GSPC_Open","GSPC_High","GSPC_Low","GSPC_Close","GSPC_Adj Close","EURUSDCHAN_Volume","year","EMA21","EMA63","EMA252","bollingerSMA_MVS","bollingerSMA_MVM","bollingerSMA_MVL","bollingerSTD_MVS","bollingerSTD_MVM","bollingerSTD_MVL","Upper_MVS","Lower_MVS","Upper_MVM","Lower_MVM","Upper_MVL","Lower_MVL","MACD","MOM63","RSI63","RSI252","MA21","MA63","MA252"]

model = auto_arima(df_train.BT_Close, exogenous=df_train[exogenous_features], trace=True, error_action="ignore", suppress_warnings=True)
model.fit(df_train.BT_Close, exogenous=df_train[exogenous_features])

forecast = model.predict(n_periods=len(df_valid), exogenous=df_valid[exogenous_features])
df_valid["Forecast_ARIMAX"] = forecast

df_valid[["BT_Close", "Forecast_ARIMAX"]].plot(figsize=(14, 7))

print("RMSE of Auto ARIMAX:", np.sqrt(mean_squared_error(df_valid.BT_Close, df_valid.Forecast_ARIMAX)))
print("\nMAE of Auto ARIMAX:", mean_absolute_error(df_valid.BT_Close, df_valid.Forecast_ARIMAX))
