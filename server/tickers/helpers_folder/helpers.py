import yfinance as yf
import pandas as pd
import os
from datetime import datetime
import datetime as dat


def my_path(outname: str):
    outdir = './media/stock_dfs'
    new_name = f'{outname}.csv'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    return os.path.join(outdir, new_name)


def check_if_file_exists(ticker: str):
    return False if not os.path.exists(my_path(ticker)) else True





def get_stock_data(ticker: str,
                   start: str = "2010-1-1",
                   end: datetime = datetime.today(),
                   period="10y",
                   use_period=False
                   ):
    ticker_data = yf.Ticker(ticker)
    if use_period:
        df = ticker_data.history(period=period)
    else:
        df = ticker_data.history(period='id', start=start, end=end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    """
    if not os.path.exists(('media/stocks_dfs/')):
        os.makedirs('media/stocks_dfs/')
    """

    df.to_csv(my_path(ticker))


def read_stock_data(ticker: str, start: str = "2010-1-1", end: datetime = datetime.today(),
                    updated: bool = True) -> pd.DataFrame:
    if updated or not os.path.exists(my_path(ticker)):
        get_stock_data(ticker, start, end)

    df = pd.read_csv(my_path(ticker), index_col='Date')

    if 'Stock Splits' in df.columns:
        df.drop(['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'],  axis=1, inplace=True)
    else:
        df.drop(['Open', 'High', 'Low', 'Volume'],  axis=1,inplace=True)
    df.rename(columns={'Close': ticker}, inplace=True)

    return df

