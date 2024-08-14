import decimal

from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Q

from datetime import datetime
import numpy as np
from decimal import Decimal

import yfinance as yf
import pandas as pd
import openpyxl
from .helpers import read_stock_data, get_stock_data
from .StockManager import StockManager
from accounts.models import Profile
from .manager import PortfolioManager, TickerManager
from .ticker_helper import TickerHelper

User = get_user_model()

class Indices(models.Model):
    title = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)
    simply_return = models.DecimalField(max_digits=30, decimal_places=3, default=0, help_text='Simply Rate of Return')

    def save(self, *args, **kwargs):
        df: pd.DataFrame = yf.download(self.code, start='1997-01-01', end=datetime.now())
        df['simply_return'] = (df['Close'] / df['Close'].shift(1)) - 1
        self.simply_return = round(df['simply_return'].mean() * 250, 2)*100

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TickerCategory(models.Model):
    title = models.CharField(max_length=240, unique=True)
    key_words = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=240)

    def __str__(self):
        return self.title


class Ticker(models.Model):
    INDICES = (
        ('^GSPC', 'SP500'),
        ('^IXIC', 'NASDAQ'),
        ('^GDAXI', 'GERMAN_DAX'),
        ('^FTSE', 'LONDON_FTSE')
    )
    ticker_category = models.ForeignKey(TickerCategory, blank=True, null=True, on_delete=models.SET_NULL)
    updated = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=200, null=True)
    ticker = models.CharField(max_length=200, null=True)
    indices = models.CharField(max_length=10, choices=INDICES, default="^GSPC"
                               )
    beta = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True)
    coverage = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    market_variance = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    camp = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    price = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    price_avg = models.DecimalField(max_digits=30, decimal_places=3, default=0)

    simply_return = models.DecimalField(max_digits=30, decimal_places=3, default=0, help_text='Simply Rate of Return')
    log_return = models.DecimalField(max_digits=30, decimal_places=8, default=0, help_text='Log Return')
    standard_deviation = models.DecimalField(max_digits=30, decimal_places=8, default=0)
    sharp = models.DecimalField(max_digits=30, decimal_places=8, default=0)

    prediction = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    date_predict = models.DateField(blank=True, null=True)

    objects = models.Manager()
    my_query = TickerManager()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        market = self.indices if self.indices else "^GSPC"
        helper = TickerHelper(self.ticker, market)
     
        data = helper.calculate_values()
        self.price = data['price']
        self.simply_return = data['simply_return']
        self.beta = data['beta']
        self.log_return = data['log_return']
        self.market_variance = data['market_variance']
        # self.prediction = float(self.predict_next_day())
      
        # self.date_predict = datetime.now() + timedelta(days=1)
        # self._refresh_ticker(is_updated=True)
        
        super().save(*args, **kwargs)

    def _refresh_ticker(self, is_updated: bool = True):
        indice, ticker = self.indices, self.ticker
        ticker_df = read_stock_data(str(ticker), updated=is_updated)
        try:
            ticker_df['log_return'] = np.log(ticker_df[ticker] / ticker_df[ticker].shift(1))
            log_return = (ticker_df['log_return'].mean() * 250) * 100
            self.log_return = log_return

            # calculate simply return
            ticker_df['simply_return'] = (ticker_df[ticker] / ticker_df[ticker].shift(1)) - 1
            simply_return = (ticker_df['simply_return'].mean() * 250) * 100
            self.simply_return = simply_return
            self.updated = datetime.now()

        except:
            print('Database not exists')
            return None

    def get_absolute_url(self):
        return reverse('ticker_detail', kwargs={'pk': self.id })

    @staticmethod
    def filter_data(qs, request):
        q = request.GET.get('q', None)
        if q:
            qs = qs.filter(Q(title__icontains=q) |
                           Q(ticker__icontains=q)
                           ).distinct()

        return qs

    def force_data(self):
        TickerDataFrame.objects.filter(ticker=self).delete()
        df: pd.DataFrame = yf.download(self.ticker, start='2010-01-01', end=datetime.now())
        df.reset_index(inplace=True)
        df['pct_change'] = ((df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1))
        print(df)
        for _, row in df.iterrows():
            try:
                pct_change = row['pct_change']
                TickerDataFrame.objects.create(date=row['Date'],
                                               close=Decimal(row['Close']),
                                               pct_change=pct_change,
                                               ticker=self
                                               )
            except:
                TickerDataFrame.objects.create(date=row['Date'],
                                              close=Decimal(row['Close']),
                                              pct_change=0,
                                              ticker=self
                                              )

    def _create_dataframe(self):
        qs = self.ticker_df.all()
        qs.delete()

        df: pd.DataFrame = yf.download(self.ticker, start='2010-01-01', end=datetime.now())
        df.reset_index(inplace=True)
        df['pct_change'] = ((df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1))
        print(df)
        for _, row in df.iterrows():
            pct_change = row['pct_change'] if isinstance(row['pct_change'], decimal.Decimal) else 0
            try:
                TickerDataFrame.objects.create(date=row['Date'],
                                                close=Decimal(row['Close']),
                                                pct_change=pct_change,
                                                ticker=self
                                                )
            except:
                continue
        """
        if not qs.exists():
            df: pd.DataFrame = yf.download(self.ticker, start='2010-01-01', end=datetime.now())
            df.reset_index(inplace=True)
            df['pct_change'] = ((df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1))
            print(df)
            for _, row in df.iterrows():
                pct_change = row['pct_change'] if isinstance(row['pct_change'], decimal.Decimal) else 0
                TickerDataFrame.objects.create(date=row['Date'],
                                               close=Decimal(row['Close']),
                                               pct_change=pct_change,
                                               ticker=self
                                               )

        else:
            qs.filter(date=datetime.now()).delete()
            df = pd.DataFrame(list(TickerDataFrame.objects.all().values()))
            df['Close'] = df['close']
            tail = df.tail(1)
            date_str = tail['date'].iloc[0].split(" ")[0]
            last_day = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
            new_df = yf.download(self.ticker, start=last_day, end=datetime.now())
            new_df.reset_index(inplace=True)
            new_df['pct_change'] = ((new_df['Close'] - new_df['Close'].shift(1)) / new_df['Close'].shift(1))

            for _, row in new_df.iterrows():
                pct_change = row['pct_change'] if isinstance(row['pct_change'], decimal.Decimal) else 0
                TickerDataFrame.objects.create(date=row['Date'],
                                               close=Decimal(row['Close']),
                                               pct_change=pct_change,
                                               ticker=self
                                               )
        """

    def calculate_percent_difference(self):
        pass

    def calculate_averages(self, df: pd.DataFrame):
        
        self.simply_return = round(df['simply_return'].mean() * 250, 2)*100
        test = (df['Close']/df['Close'].shift(1)).mean() * 250
        
        # self.log_return = round((np.log() * 100, 3)

    def calculate_rick(self, df: pd.DataFrame):
        # get the data, ticker and indice you want to compete and combine them
        sec_data = pd.DataFrame()
        sec_data[self.ticker] = df['Close']
        sec_data[self.indices] = yf.download(self.indices, start='2010-01-01', end=datetime.now())['Close']

        # get the returns
        sec_returns = np.log(sec_data/sec_data.shift(1))
        self.standard_deviation = sec_returns[self.ticker].std() * 250 ** 0.5
        cov = sec_returns.cov() * 250
        self.coverage = cov.iloc[0][1]
        self.market_variance = sec_returns[self.indices].var() * 250
        ticker_var = sec_returns[self.ticker].var() * 250
        indi_var = sec_returns[self.indices].var() * 250

        return "done"

    def predict_next_day(self):
        stock_manager = StockManager(ticker=self.ticker)
        stock_manager.load_df()
        stock_manager.scale_data()
        stock_manager.build_model(epochs=50)
        return stock_manager.predict_the_future()


    @staticmethod
    def create_ticker_database():
        dataframe = openpyxl.load_workbook("tickers/media/companies.xlsx")
        dataframe1 = dataframe.active
        for row in dataframe1:
            print(row[0].value, row[1].value, row[2].value)
            obj = Ticker.objects.create(ticker=row[0].value, title=row[1].value)
            print(f"{obj} is created!")



class TickerDataFrame(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, related_name="ticker_df")
    date = models.CharField(max_length=220, default="")
    close = models.DecimalField(max_digits=10, decimal_places=2)
    pct_change = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date', ]
        unique_together = ["ticker", "date"]

    def __str__(self):
        return self.date


class Portfolio(models.Model):
    is_public = models.BooleanField(default=False)
    date_investment = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    annual_returns = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    variance = models.DecimalField(max_digits=200, decimal_places=150, default=0)
    starting_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    withdraw_value = models.DecimalField(max_digits=15, decimal_places=4, default=0)

    expected_portfolio_return = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    expected_portfolio_volatility = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    expected_portfolio_variance = models.DecimalField(max_digits=15, decimal_places=4, default=0)

    my_query = PortfolioManager()
    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id:
            qs: models.QuerySet = self.port_tickers.all()
            if qs.exists():
                # self.calculate_data()
                self.starting_investment: float = qs.aggregate(Sum('starting_investment'))['starting_investment__sum']
                self.current_value: float = qs.aggregate(Sum('current_value'))['current_value__sum'] if qs.exists() else 0
                self.withdraw_value = qs.aggregate(Sum("close_value"))["close_value__sum"] 
                # self.expected_portfolio_return, self.expected_portfolio_variance, self.expected_portfolio_volatility = self.calculate_returns_and_volatility()

        super().save(*args, **kwargs)
        user = self.user
        profile_qs = Profile.objects.filter(user=user).all()
        if profile_qs.exists():
            profile_qs.first().save()


    def show_diff(self):
        return self.current_value - self.starting_investment
    
    def show_diff_percent(self):
        return (self.current_value/self.starting_investment) *100 if self.starting_investment != 0 else 0

    def calculate_data(self):
        qs = self.port_tickers.all()
        weights, df = [], pd.DataFrame()

        # calculate the weights and get the ticker code
        for ticker in qs:
            weights.append(round(ticker.current_value/self.current_value if self.current_value !=0 else 0, 2))
            new_df = pd.DataFrame(list(TickerDataFrame.objects.filter(ticker=ticker.ticker)))
            df = df.join(new_df, how="outer")
        weights = np.array(weights)


        log_returns = np.log(df / df.shift(1))
        mean = log_returns.mean()  # *250

        self.expected_portofolio_return = Decimal(np.sum(weights * mean)) * 250 or 0
        self.expected_portfolio_variance = np.dot(weights.T, np.dot(log_returns.cov() * 250, weights)) or 0
        self.expected_portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))) or 0

    def monthly_realised_volatility(self, df: pd.DataFrame):
        df_rv = df.groupby(pd.Grouper('M')).apply(self.realized_volatility)
        df_rv.rename(columns={'Close': 'rv'}, inplace=True)

    @staticmethod
    def realized_volatility(x: pd.DataFrame):
        return np.sqrt(np.sum(x**2))

    def get_edit_url(self):
        return reverse('portfolio', kwargs={'port_id': self.id})
    

    def efficient_frontier(self):
        tickers = [ticker.ticker for ticker in self.port_tickers.filter(is_sell=False)]
        assets = [ticker.ticker for ticker in tickers]

        df = pd.DataFrame()
        for ticker in assets:
            new_df = read_stock_data(ticker)
            df = new_df if df.empty else df.join(new_df, how="outer")

        log_returns = np.log(df/df.shift(1))
        mean = log_returns.mean() * 250
        cov = log_returns.cov()
        corr = log_returns.corr()

        num_assets = len(assets)
        pfolio_returns, pfolio_volatilies, total_weights, total_money = [], [], [], []

        for x in range(1, 1000):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            pfolio_returns.append(np.sum(weights * log_returns.mean()) * 250)
            pfolio_volatilies.append(np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))))
            total_weights.append(weights)

            current_money = []
            for weight in weights:
                current_money.append(round(float(self.starting_investment) * float(round(weight, 4)), 2))
            total_money.append(current_money)

        pfolio_returns = np.array(pfolio_returns)
        pfolio_volatilies = np.array(pfolio_volatilies)
        return [total_weights, pfolio_volatilies, pfolio_returns, total_money]



class UserTicker(models.Model):
    updated = models.DateTimeField(blank=True, null=True)
    date_buy = models.DateTimeField(blank=True, null=True)
 
    is_sell = models.BooleanField(default=False)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, null=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, null=True, related_name='port_tickers')

    starting_investment = models.DecimalField(max_digits=30, decimal_places=8, default=0)
    current_value = models.DecimalField(max_digits=30, decimal_places=8, default=0)
    close_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    qty = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    starting_value_of_ticker = models.DecimalField(max_digits=30, decimal_places=8, default=0)
    current_value_of_ticker = models.DecimalField(max_digits=30, decimal_places=8, default=0)
    weight = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.is_sell:
            self.qty = self.starting_investment/self.starting_value_of_ticker if self.starting_value_of_ticker != 0 else 0
            self.current_value_of_ticker = self.ticker.price
            self.current_value = Decimal(self.qty) * Decimal(self.current_value_of_ticker)
        else:
            self.close_value = self.current_value
        super().save(*args, **kwargs)
        self.portfolio.save()

    def tag_diff(self):
        return (self.current_value_of_ticker - self.starting_value_of_ticker) * self.qty

    def tag_diff_pct(self):
        return ((self.current_value_of_ticker/self.starting_value_of_ticker))* 100 if self.starting_value_of_ticker != 0 else 0


    def tag_ticker_title(self):
        return f"{self.ticker.title}"