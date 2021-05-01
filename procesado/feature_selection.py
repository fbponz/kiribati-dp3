from sklearn.datasets import load_boston
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso

dataframe = pd.read_csv("../data/data_raw.csv")
print(dataframe.head())

cor = dataframe.corr()
cor_target = abs(cor["BT_Close"])
print('\n Feature mas relevantes \n')
relevant_features = cor_target[cor_target>0.5]
print(relevant_features)
print('\n Feature menos relevantes \n')
non_relevant_features = cor_target[cor_target<0.5]
print(non_relevant_features)
for index, value in non_relevant_features.items():
    dataframe.drop(columns=index, axis=1, inplace=True)

print(dataframe.head())
dataframe.to_csv("../data/data_filtered.csv")

