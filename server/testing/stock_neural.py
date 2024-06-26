import pandas as pd
import numpy as np
import yfinance as yf
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

ticker = "MSFT"

data = yf.download(ticker, start='2000-01-01', end='2021-01-01')
data = generate_features(data)
data = data.dropna()

split_date = '2020-01-01'
train_data = data[:split_date]
test_data = data[split_date:]


X_train = train_data.drop(["Close"], axis=1).values
y_train = train_data['Close'].values

X_test = test_data.drop(['Close'], axis=1).values
y_test = test_data['Close'].values

# Step 4: Apply StandardScaler to scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 5: Build a Sequential model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(64, activation='relu'),
    Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Step 6: Train the model
model.fit(X_train_scaled, y_train, epochs=200, batch_size=32, validation_split=0.2)

# Step 7: Evaluate the model
test_loss = model.evaluate(X_test_scaled, y_test)
print("Test Loss:", test_loss)

predictions = model.predict(X_test_scaled)[:, 0]
print("Pred:", predictions)
print(f'MSE: {mean_squared_error(y_test, predictions):.3f}')
print(f'MAE: {mean_absolute_error(y_test, predictions):.3f}')
print(f'R^2: {r2_score(y_test, predictions):.3f}')




