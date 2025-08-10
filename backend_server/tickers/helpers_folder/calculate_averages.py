import pandas as pd


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