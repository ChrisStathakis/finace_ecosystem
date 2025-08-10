import decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Q
from datetime import datetime
from decimal import Decimal
import yfinance as yf
import pandas as pd
import requests

from .manager import TickerManager
from .helpers_folder.StockManager import TickerHelper


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
    ticker = models.CharField(max_length=200, null=True, unique=True)
    indices = models.CharField(max_length=10, choices=INDICES, default="^GSPC"
                               )
    beta = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True)
    coverage = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    market_variance = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    camp = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    price = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    price_change = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0,
                                       help_text="Price change last day")
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else ""
    
    def soft_update(self):
        # update basic data like price now etc

        market = self.indices if self.indices else "^GSPC"
        helper = TickerHelper(str(self.ticker), market)
        helper.download_data(is_period=True, period="7d")
        data = helper.calculate_values()
        self.price = data['price']
        self.price_change = data["price_change"]
        self.save()

    def hard_update(self):
        # update and calculate most of the ticker analysis data
        market = self.indices if self.indices else "^GSPC"
        helper = TickerHelper(str(self.ticker), market)
        helper.download_data(is_period=True, period="10y")
        data = helper.calculate_values()
        self.log_return = data["log_return"]
        self.price = data['price']
        self.simply_return = data['simply_return']
        self.beta = data['beta']
        self.market_variance = data['market_variance']
        self.price_change = data['price_change']
        self.save()

    def sentimental_analysis_update(self):
        # update wiki data and rss
        self.wikipedia_url = self.find_wikipedia_url()

    @staticmethod
    def search_entities(entities: list):
        tags = Tags.objects.filter(title__in=entities)
        tickers_tag = Ticker.objects.filter(ticker_tags__in=tags)
        tickers = Ticker.objects.filter(title__in=entities)
        return tickers | tickers_tag

    def find_wikipedia_url(self):
        url = f"https://en.wikipedia.org/w/index.php?search={self.title}"
        response = requests.get(url)
        return response.url

    def create_tags(self):
        market = self.indices if self.indices else "^GSPC"
        ticker_helper = TickerHelper(ticker=self.ticker, market=market)
        results = ticker_helper.analyze_ticker_wiki(self.wikipedia_url)
        for result in results:
            new_result, created = Tags.objects.get_or_create(title=result[0], label=result[1])
            self.ticker_tags.add(new_result)

    def get_absolute_url(self):
        return reverse('tickers:detail', kwargs={'pk': self.id})

    @staticmethod
    def filter_data(qs, request):
        q = request.GET.get('q', None)
        if q:
            qs = qs.filter(Q(title__icontains=q) |
                           Q(ticker__icontains=q)
                           ).distinct()

        return qs


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

    def _create_dataframe(self,
                          is_period: bool = True,
                          period: str = "10y",
                          date_start: str = "",
                          date_end: str = ""
                          ):
        qs = TickerDataFrame.objects.filter(ticker=self.ticker)
        helper = TickerHelper(str(self.ticker), str(self.ticker.indices))
        df = helper.read_data(update_data=True, is_period=is_period, period=period, date_start=date_start,
                              date_end=date_end)
        df['pct_change'] = ((df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1))
        for _, row in df.iterrows():
            pct_change = row['pct_change'] # if isinstance(row['pct_change'], decimal.Decimal) else 0
            if not qs.filter(date=row['Date']).exists():
                TickerDataFrame.objects.create(date=row['Date'],
                                               close=Decimal(row['Close']),
                                               pct_change=pct_change,
                                               ticker=self
                                               )
            else:
                continue






