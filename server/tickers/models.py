import decimal
from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Q
from datetime import datetime
from datetime import timedelta
import numpy as np
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
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
    label = models.CharField(max_length=240)

    class Meta:
        unique_together = ["title", "label"]

    def __str__(self):
        return self.title


class Ticker(models.Model):
    INDICES = (
        ('^GSPC', 'SP500'),
        ('^IXIC', 'NASDAQ'),
        ('^GDAXI', 'GERMAN_DAX'),
        ('^FTSE', 'LONDON_FTSE')
    )
    created = models.BooleanField(default=False)
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
    wikipedia_url = models.URLField(blank=True, null=True)
    prediction = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    date_predict = models.DateField(blank=True, null=True)
    ticker_tags = models.ManyToManyField(Tags)
    objects = models.Manager()
    my_query = TickerManager()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        self.wikipedia_url = self.find_wikipedia_url()
        if self.id:
            self.create_tags()

        market = self.indices if self.indices else "^GSPC"
        helper = TickerHelper(self.ticker, market)

        data = helper.calculate_values()
        self.price = data['price']
        self.simply_return = data['simply_return']
        self.beta = data['beta']
        self.log_return = data['log_return']
        self.market_variance = data['market_variance']
        self.prediction = float(self.predict_next_day())

        self.date_predict = datetime.now() + timedelta(days = 1)
        # self._refresh_ticker(is_updated=True)
        self.created = True
        super().save(*args, **kwargs)



    @staticmethod
    def search_entities(entities: list):
        tags = Tags.objects.filter(title__in=entities)
        tickers_tag = Ticker.objects.filter(ticker_tags__in=tags)
        tickers = Ticker.objects.filter(title__in=entities)
        return tickers | tickers_tag

    def find_wikipedia_url(self):
        url = f"https://en.wikipedia.org/w/index.php?search={self.title}"
        response = requests.get(url)
        print("--------------")
        print(response.url)
        print(url)
        print("------------")
            
        return response.url
        if not self.wikipedia_url:
            url = f"https://en.wikipedia.org/w/index.php?search={self.title}"
            response = requests.get(url)
            print("--------------")
            print(response.url)
            print(url)
            print("------------")
            
            return response.url
        return self.wikipedia_url



    def create_tags(self):
        market = self.indices if self.indices else "^GSPC"
        ticker_helper = TickerHelper(ticker=self.ticker, market=market)
        results = ticker_helper.analyze_ticker_wiki(self.wikipedia_url)
        for result in results:
            new_result, created = Tags.objects.get_or_create(title=result[0], label=result[1])
            self.ticker_tags.add(new_result)


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
        return reverse('tickers:detail', kwargs={'pk': self.id })

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

        df: pd.DataFrame = yf.download(self.ticker, start='2010-01-01', end=datetime.now(), period='1d')
        df.reset_index(inplace=True)
        df['pct_change'] = ((df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1))
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

    def calculate_MACD(self):
        qs = self.ticker_df.all()
        data = pd.DataFrame(
            list(qs.values())
        )
        data["ema12"] = data["close"].ewm(span=12).mean()
        data["ema26"] = data["close"].ewm(span=26).mean()
        data["macd"] = data["ema12"] - data["ema26"]

        data["macd_signal"] = data['macd'].ewm(span=9).mean()
        data["macd_histogram"] = data["macd"] - data["macd_signal"]
        data['regime'] = pd.NA

        for i in range(0, len(data)-1):
            if data['macd_histogram'][i] >= 0:
                data['regime'][i+1] = 1
            else:
                data['regime'][i+1] = 0

        return data


    @staticmethod
    def create_ticker_database():
        dataframe = openpyxl.load_workbook("tickers/media/companies.xlsx")
        dataframe1 = dataframe.active
        for row in dataframe1:
            obj = Ticker.objects.create(ticker=row[0].value, title=row[1].value)




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

