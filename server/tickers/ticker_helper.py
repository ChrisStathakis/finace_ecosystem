import yfinance as yf
import pandas as pd
import os
import datetime
import numpy as np


class TickerHelper:

    def __init__(self, ticker, market):
        self.ticker = ticker
        self.market = market
        self.price = 0

    def download_data(self,
                      ticker='',
                      start='2010-1-1',
                      end=datetime.datetime.today(),
                      ):
        ticker = ticker if ticker != "" else self.ticker

        df = yf.Ticker(ticker)
        df = df.history(period='id', start=start, end=end)
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        if not os.path.exists('media/stock_df'):
            os.makedirs("media/stock_df")
        df.to_csv(f"media/stock_df/{ticker}.csv")

    def read_data(self, update_data=True):
        if update_data:
            self.download_data()
        df = pd.read_csv(f'media/stock_df/{self.ticker}.csv', index_col='Date')
        if 'Stock Splits' in df.columns:
            df.drop(labels=['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], axis=1, inplace=True)
        else:
            df.drop(labels=['Open', 'High', 'Low', 'Volume'], axis=1, inplace=True)

        df.rename(columns={'Close': self.ticker}, inplace=True)
        return df

    def read_market(self):
        print('Read market', self.market)
        if not os.path.exists(f'media/stock_df/{self.market}.csv'):
            self.download_data(self.market)

        df = pd.read_csv(f'media/stock_df/{self.market}.csv', index_col='Date')
        if 'Stock Splits' in df.columns:
            df.drop(labels=['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], axis=1, inplace=True)
        else:
            df.drop(labels=['Open', 'High', 'Low', 'Volume'], axis=1, inplace=True)

        df.rename(columns={'Close': self.market}, inplace=True)

        return df

    def read_ticker(self,
                    code: str,  # **ticker code
                    start: str = '2010-1-1',  # the start day for ticker history
                    end: str = datetime.datetime.today()  # the last day for ticker history
                    ) -> pd.DataFrame:
        df = yf.Ticker(code)
        df = df.history(period='id', start=start, end=end)
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        if not os.path.exists('media/stock_df'):
            os.makedirs("media/stock_df")
        df.to_csv(f"media/stock_df/{code}.csv")
        self.download_data(code)

        df = pd.read_csv(f"media/stock_df/{code}.csv", index_col='Date')
        if 'Stock Splits' in df.columns:
            df.drop(labels=['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], axis=1, inplace=True)
        else:
            df.drop(labels=['Open', 'High', 'Low', 'Volume'], axis=1, inplace=True)

        df.rename(columns={'Close': code}, inplace=True)
        return df

    def calculate_camp(self, group):
        data = self.read_data(update_data=False)
        stock_return = data[self.ticker].pct_change().dropna().mean()
        market_return = self.read_ticker(group)[group].pct_change()

    def calculate_values(self) -> dict:
        # group => the code of the market you want to go against
        group, tic = [self.market, self.ticker]
        stock_data, indice_data = [self.read_data(self.ticker), self.read_market()]
        stock_return, indice_return = [stock_data[tic].pct_change(), indice_data[group].pct_change()]

        indice_data['daily_rtn'] = indice_return
        stock_data['daily_rtn'] = stock_return

        stock_data['log_return'] = np.log(stock_data[tic] / stock_data[tic].shift(1))
        log_return = (stock_data['log_return'].mean() * 250) * 100
        stock_data['simply_return'] = (stock_data[tic] / stock_data[tic].shift(1)) - 1
        simply_return = (stock_data['simply_return'].mean() * 250) * 100

        indice_return, stock_return = [indice_return.dropna(), stock_return.dropna()]

        market_variance = indice_return.var()
        covariance = stock_return.cov(indice_return)
        print(market_variance, covariance)

        beta = covariance / market_variance if market_variance != 0 else 0

        price = round(float(stock_data[tic].iloc[-1]), 8) if isinstance(stock_data[tic].iloc[-1], float) else 0
        self.price = 0 if np.isnan(price) else price if isinstance(price, str) else price

        return {
            'log_return': log_return,
            "price": price,
            "simply_return": simply_return,
            "beta": beta,
            "market_variance": market_variance,

        }




