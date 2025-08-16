import pandas as pd
import quantstats as qs
import numpy as np
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDRegressor
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader
import spacy, os, datetime, requests
from bs4 import BeautifulSoup
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import torch
from tickers.helpers_folder.calculate_averages import *


nlp = spacy.load("en_core_web_sm")


class TickerHelper:

    def __init__(self, ticker: str, market: str):
        self.ticker = ticker
        self.market = market
        self.price = 0

    @staticmethod
    def analyze_ticker_wiki(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div
        content = soup.find(id="mw-content-text")

        # Extract text from paragraphs
        text = ''.join([p.get_text() for p in content.find_all('p')])
        doc = nlp(text)
        results = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"]:
                results.append([ent.text, ent.label_])
        return results

    def download_data(self,
                      ticker='',
                      date_start='2010-1-1',
                      date_end=datetime.datetime.today(),
                      is_period=False,
                      period="10y"
                      ):
        ticker = ticker if ticker != "" else self.ticker

        df = yf.Ticker(ticker)
        if is_period:
            df = df.history(period=period)
        else:
            df = df.history(start=date_start, end=date_end)
        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)

        if not os.path.exists('media/stock_df'):
            os.makedirs("media/stock_df")
        df.to_csv(f"media/stock_df/{ticker}.csv")

    def read_data(self, update_data=True,
                  is_period: bool = False,
                  period: str = "10y",
                  date_start: str = "",
                  date_end: str = ""
                  ):
        if update_data:
            self.download_data(ticker=self.ticker, is_period=is_period, period=period, date_start=date_start,
                               date_end=date_end)
        df = pd.read_csv(f'media/stock_df/{self.ticker}.csv', index_col='Date')
        if 'Stock Splits' in df.columns:
            df.drop(labels=['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], axis=1, inplace=True)
        else:
            df.drop(labels=['Open', 'High', 'Low', 'Volume'], axis=1, inplace=True)

        df.rename(columns={'Close': self.ticker}, inplace=True)
        return df

    def read_market(self):
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
        # add new method to calaculate data
        end_date = pd.Timestamp.today().normalize()
        start_date = end_date - pd.DateOffset(years=10)
        qs_ticker_df = qs.utils.download_returns(self.ticker).loc[start_date:end_date]
        qs_market_df = qs.utils.download_returns(self.market).loc[start_date:end_date]
        qs_merged_df = pd.concat([qs_ticker_df, qs_market_df], join="outer", axis=1)
        qs_ticker_df_no_index = qs_ticker_df.reset_index(drop=True)
        qs_market_df_no_index = qs_market_df.reset_index(drop=True)
        X, y = qs_market_df_no_index.values.reshape(-1, 1), qs_ticker_df_no_index.values.reshape(-1, 1)
        linreg = LinearRegression().fit(X, y)
        beta = linreg.coef_[0]
        alpha = linreg.intercept_
        print("qs beta", beta)

        # group => the code of the market you want to go against
        group, tic = [self.market, self.ticker]
        stock_data, indice_data = [self.read_data(update_data=False), self.read_market()]
        stock_return, indice_return = [stock_data[tic].pct_change(), indice_data[group].pct_change()]
        indice_data['daily_rtn'] = indice_return
        stock_data['daily_rtn'] = stock_return

        stock_data['log_return'] = np.log(stock_data[tic] / stock_data[tic].shift(1))
        log_return = (stock_data['log_return'].mean() * 250) * 100
        stock_data['simply_return'] = (stock_data[tic] / stock_data[tic].shift(1)) - 1
        simply_return = (stock_data['simply_return'].mean() * 250) * 100

        indice_return, stock_return = [indice_return.dropna(), stock_return.dropna()]

        market_variance = indice_return.var()
        coverage = qs_merged_df.cov()
        correlation = qs_merged_df.corr()
        beta = coverage / market_variance if market_variance != 0 else 0

        price = round(float(stock_data[tic].iloc[-1]), 8) if isinstance(stock_data[tic].iloc[-1], float) else 0
        self.price = 0 if np.isnan(price) else price if isinstance(price, str) else price
        price_change = ((stock_data[tic].iloc[-1] - stock_data[tic].iloc[-2]) / stock_data[tic].iloc[-1]) * 100

        return {
            'log_return': log_return,
            "price": price,
            "simply_return": simply_return,
            "beta": beta,
            "alpha": alpha,
            "sharp": qs.stats.sharpe(qs_ticker_df),
            "market_variance": market_variance,
            "price_change": price_change,
            "correlation": correlation,
            "coverage": coverage

        }


class StockManager(nn.Module):

    def __init__(self, ticker: str) -> None:
        super().__init__()
        self.ticker = ticker
        self.scaler = StandardScaler()
        self.load_df()
        self.model = nn.Sequential(
            nn.Linear(self.X_train.shape[1], 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        self.nlp = spacy.load("en_core_web_sm")

    def analyze_ticker_wiki(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content div
        content = soup.find(id="mw-content-text")

        # Extract text from paragraphs
        text = ''.join([p.get_text() for p in content.find_all('p')])
        doc = self.nlp(text)
        results = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"]:
                results.append([ent.text, ent.label_])

        return results



    def load_df(self):
        ten_years_ago = datetime.now() - relativedelta(years=10)
        data = yf.download(self.ticker, start=ten_years_ago, end=datetime.now())
        data = add_original_feature(data)
        data = add_avg_price(data)
        data = add_avg_volume(data)
        data = add_std_price(data)
        data = add_std_volume(data)
        data = add_return_feature(data)
        data = data.dropna(axis=0)

        self.data = data
        last_20_percent = int(len(data) * 0.2)
        train_data = data.head(len(data) - last_20_percent)
        test_data = data.tail(last_20_percent)

        self.X_train = train_data.drop(columns=["Close"]).values
        self.y_train = train_data["Close"].values
        self.X_test = test_data.drop(columns=["Close"]).values
        self.y_test = test_data["Close"].values

    def scale_data(self):
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

    def build_model(self, epochs: int = 10):
        self.scale_data()

        # Convert to PyTorch tensors
        X_train_tensor = torch.tensor(self.X_train_scaled, dtype=torch.float32)
        y_train_tensor = torch.tensor(self.y_train, dtype=torch.float32).unsqueeze(1)
        X_test_tensor = torch.tensor(self.X_test_scaled, dtype=torch.float32)
        y_test_tensor = torch.tensor(self.y_test, dtype=torch.float32).unsqueeze(1)

        train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        self.train()  # Set model to training mode
        for epoch in range(epochs):
            total_loss = 0
            for X_batch, y_batch in train_loader:
                optimizer.zero_grad()
                outputs = self.model(X_batch)
                loss = criterion(outputs, y_batch)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {total_loss/len(train_loader):.4f}")

        # Evaluation
        self.eval()  # Set model to evaluation mode
        with torch.no_grad():
            predictions = self.model(X_test_tensor).squeeze().numpy()

        print(f"MSE: {mean_squared_error(self.y_test, predictions):.3f}")
        print(f"MAE: {mean_absolute_error(self.y_test, predictions):.3f}")
        print(f"R^2: {r2_score(self.y_test, predictions):.3f}")

    def predict_the_future(self):
        self.eval()
        X_test_tensor = torch.tensor(self.X_test_scaled, dtype=torch.float32)
        with torch.no_grad():
            predictions = self.model(X_test_tensor).numpy()
        print(predictions)
        return predictions[-1][0]  # Returning last prediction