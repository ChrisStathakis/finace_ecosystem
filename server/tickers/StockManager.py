import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDRegressor
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def add_original_feature(df: pd.DataFrame):
    df['open_1'] = df['Open'].shift(1)
    df['close_1'] = df['Close'].shift(1)
    df['high_1'] = df['High'].shift(1)
    df["low_1"] = df['Low'].shift(1)
    df['volume_1'] = df['Volume'].shift(1)

    return df


def add_avg_price(df: pd.DataFrame):
    df['avg_price_5'] = df["Close"].rolling(5).mean().shift(1)
    df['avg_price_30'] = df["Close"].rolling(21).mean().shift(1)
    df['avg_price_365'] = df["Close"].rolling(252).mean().shift(1)

    df['ratio_avg_price_5_30'] = df['avg_price_5'] / df['avg_price_30']
    df['ratio_avg_price_5_365'] = df['avg_price_5'] / df['avg_price_365']
    df['ratio_avg_price_30_365'] = df['avg_price_30'] / df['avg_price_365']

    return df


def add_avg_volume(df: pd.DataFrame):
    df['avg_volume_5'] = df['Volume'].rolling(5).std().shift(1)
    df['avg_volume_30'] = df['Volume'].rolling(21).std().shift(1)
    df['avg_volume_365'] = df['Volume'].rolling(252).std().shift(1)

    df['ratio_avg_volume_5_30'] = df['avg_volume_5'] / df['avg_volume_30']
    df['ratio_avg_volume_5_365'] = df['avg_volume_5'] / df['avg_volume_365']
    df['ratio_avg_volume_30_365'] = df['avg_volume_30'] / df['avg_volume_365']

    return df


def add_std_price(df: pd.DataFrame):
    df['std_price_5'] = df['Close'].rolling(5).std().shift(1)
    df['std_price_30'] = df['Close'].rolling(21).std().shift(1)
    df['std_price_365'] = df['Close'].rolling(252).std().shift(1)
    df['ratio_std_price_5_30'] = df['std_price_5'] / df['std_price_30']
    df['ratio_std_price_5_365'] = df['std_price_5'] / df['std_price_365']
    df['ratio_std_price_30_365'] = df['std_price_30'] / df['std_price_365']
    return df


def add_std_volume(df: pd.DataFrame):
    df['std_volume_5'] = df['Volume'].rolling(5).std().shift(1)
    df['std_volume_30'] = df['Volume'].rolling(21).std().shift(1)
    df['std_volume_365'] = df['Volume'].rolling(252).std().shift(1)
    df['ratio_std_volume_5_30'] = df['std_volume_5'] / df['std_volume_30']
    df['ratio_std_volume_5_365'] = df['std_volume_5'] / df['std_volume_365']
    df['ratio_std_volume_30_365'] = df['std_volume_30'] / df['std_volume_365']

    return df


def add_return_feature(df: pd.DataFrame):
    df['return_1'] = ((df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1)).shift(1)
    df['return_5'] = ((df['Close'] - df['Close'].shift(5)) / df['Close'].shift(5)).shift(1)
    df['return_30'] = ((df['Close'] - df['Close'].shift(21)) / df['Close'].shift(21)).shift(1)
    df['return_365'] = ((df['Close'] - df['Close'].shift(252)) / df['Close'].shift(252)).shift(1)
    df['moving_avg_5'] = df['return_1'].rolling(5).mean().shift(1)
    df['moving_avg_30'] = df['return_1'].rolling(21).mean().shift(1)
    df['moving_avg_365'] = df['return_1'].rolling(252).mean().shift(1)

    return df


def generate_features(df: pd.DataFrame):
    new_df = add_original_feature(df)
    new_df = add_avg_price(new_df)
    new_df = add_avg_volume(new_df)
    new_df = add_std_price(new_df)
    new_df = add_std_volume(new_df)
    new_df = add_return_feature(new_df)
    df_new = new_df.dropna(axis=0)
    return df_new




class StockManager:

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.scaler = StandardScaler()


    def load_df(self):
        ten_year_ago = datetime.now() - relativedelta(years=10)
        split_date = datetime.now() - relativedelta(years=2)
        data = yf.download(self.ticker, start=ten_year_ago, end=datetime.now())
        data = add_original_feature(data)
        data = add_avg_price(data)
        data = add_avg_volume(data)
        data = add_std_price(data)
        data = add_std_volume(data)
        data = add_return_feature(data)
        data = data.dropna(axis=0)
        data.dropna()
        self.data = data
        
        train_data = data[:split_date]
        test_data = data[split_date:]


        self.X_train = train_data.drop(["Close"], axis=1).values
        self.y_train = train_data['Close'].values

        self.X_test = test_data.drop(['Close'], axis=1).values
        self.y_test = test_data['Close'].values


    
    def scale_data(self):
        scaler = self.scaler
        self.X_train_scaled = scaler.fit_transform(self.X_train)
        self.X_test_scaled = scaler.transform(self.X_test)


    def build_model(self, epochs: int = 100):
        model = self.model = Sequential([
            Dense(64, activation='relu', input_shape=(self.X_train_scaled.shape[1],)),
            Dense(64, activation='relu'),
            Dense(1)
        ])

        model.compile(optimizer="adam", loss="mse")

        model.fit(self.X_train_scaled, self.y_train, epochs=epochs, batch_size=32, validation_split=0.2)
        test_loss = model.evaluate(self.X_test_scaled, self.y_test)
        print("Test Loss:", test_loss)

        predictions = model.predict(self.X_test_scaled)[:, 0]

        print(f'MSE: {mean_squared_error(self.y_test, predictions):.3f}')
        print(f'MAE: {mean_absolute_error(self.y_test, predictions):.3f}')
        print(f'R^2: {r2_score(self.y_test, predictions):.3f}')

        self.model = model
    

    def predict_the_future(self, days: int = 5):
        data = self.data
        for _ in range(days):
            last_day = data.iloc[-1]
            last_day["Close"] = last_day["Close"] * 1.05
            X_test = last_day.drop(['Close']).values.reshape(1, -1)
            y_test = last_day["Close"] * 1.05
            scaled_next_day_features = self.scaler.transform(X_test)
            next_day_prediction = self.model.predict(scaled_next_day_features)
            print("Predict", next_day_prediction)

       


