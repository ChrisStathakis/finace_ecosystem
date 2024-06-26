import pickle
import pandas as pd


def compile_data():
    with open('sp500tickers.pickle', "rb") as f:
        tickers = pickle.load(f)
        return tickers


main_df = pd.DataFrame()
tickers = compile_data()


for ticker in tickers:
    try:
        df = pd.read_csv(f"stock_dfs/{ticker}.csv")
        df.set_index('Date', inplace=True)
        df['{}_HL_pct_diff'.format(ticker)] = (df['High'] - df['Low']) / df['Low']
        df['{}_daily_pct_chng'.format(ticker)] = (df['Close'] - df['Open']) / df['Open']
        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
    except:
        print('fail', ticker)
        continue

print(main_df.head())
main_df.to_csv('sp500_joined_closes.csv')

