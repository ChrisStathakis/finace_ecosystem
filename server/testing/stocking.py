import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

df_ms = yf.Ticker("MSFT").history(start="2022-01-01", end=None)


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


def compute_prediction(X, weights):
    """
    Compute the prediction y_hat based on current weights
    """
    predictions = np.dot(X, weights)
    return predictions


def update_weights_gd(X_train, y_train, weights, learning_rate):
    """
    Update weights by one step and return updated wights
    """
    predictions = compute_prediction(X_train, weights)
    weights_delta = np.dot(X_train.T, y_train - predictions)
    m = y_train.shape[0]
    weights += learning_rate / float(m) * weights_delta
    return weights


def compute_cost(X, y, weights):
    """
    Compute the cost J(w)
    """
    predictions = compute_prediction(X, weights)
    cost = np.mean((predictions - y) ** 2 / 2.0)
    return cost


def train_linear_regression(X_train, y_train, max_iter, learning_rate, fit_intercept=False):
    """
    Train a linear regression model with gradient descent, and return trained model
    """
    if fit_intercept:
        intercept = np.ones((X_train.shape[0], 1))
        X_train = np.hstack((intercept, X_train))
    weights = np.zeros(X_train.shape[1])
    for iteration in range(max_iter):
        weights = update_weights_gd(X_train, y_train, weights, learning_rate)
        # Check the cost for every 100 (for example) iterations
        if iteration % 100 == 0:
            print(compute_cost(X_train, y_train, weights))
    return weights


def predict(X, weights):
    if X.shape[1] == weights.shape[0] - 1:
        intercept = np.ones((X.shape[0], 1))
        X = np.hstack((intercept, X))
    return compute_prediction(X, weights)

"""
# A small example
X_train = np.array([[6], [2], [3], [4], [1], [5], [2], [6], [4], [7]])

y_train = np.array([5.5, 1.6, 2.2, 3.7, 0.8, 5.2, 1.5, 5.3, 4.4, 6.8])

weights = train_linear_regression(X_train, y_train, max_iter=100, learning_rate=0.01, fit_intercept=True)

X_test = np.array([[1.3], [3.5], [5.2], [2.8]])

predictions = predict(X_test, weights)
plt.scatter(X_train[:, 0], y_train, marker="o", c="b")
plt.scatter(X_test[:, 0], predictions, marker='*', c='k')
plt.xlabel("x")
plt.ylabel("y")
plt.show()
"""


diabetes = datasets.load_diabetes()
print(diabetes.data.shape)
num_test = 30
X_train = diabetes.data[:-num_test, :]
y_train = diabetes.target[:-num_test]

weights = train_linear_regression(X_train, y_train, max_iter=5000, learning_rate=1, fit_intercept=True)

# 296