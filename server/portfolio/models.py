import datetime

from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.urls import reverse
import numpy as np
from decimal import Decimal
import pandas as pd
from tickers.helpers import read_stock_data
from accounts.models import Profile
from tickers.manager import PortfolioManager
from tickers.models import Ticker, TickerDataFrame


User = get_user_model()
CURRENCY = settings.CURRENCY


class Portfolio(models.Model):
    is_public = models.BooleanField(default=False)
    date_investment = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="port")
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
            qs: models.QuerySet = self.port_tickers.filter(is_sell=False)

            # self.calculate_data()
            self.starting_investment: float = qs.aggregate(Sum('starting_investment'))['starting_investment__sum'] or 0
            self.current_value: float = qs.aggregate(Sum('current_value'))[
                    'current_value__sum'] if qs.exists() else 0 or 0
            self.withdraw_value = qs.aggregate(Sum("close_value"))["close_value__sum"] or 0
                # self.expected_portfolio_return, self.expected_portfolio_variance, self.expected_portfolio_volatility = self.calculate_returns_and_volatility()
        super().save(*args, **kwargs)
        user = self.user
        profile_qs = Profile.objects.filter(user=user).all()
        if profile_qs.exists():
            profile_qs.first().save()


    def show_diff(self):
        return self.current_value - self.starting_investment

    def show_diff_percent(self):
        return (self.current_value / self.starting_investment) * 100 if self.starting_investment != 0 else 0

    def calculate_data(self):
        qs = self.port_tickers.all()
        weights, df = [], pd.DataFrame()

        # calculate the weights and get the ticker code
        for ticker in qs:
            weights.append(round(ticker.current_value / self.current_value if self.current_value != 0 else 0, 2))
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
        return np.sqrt(np.sum(x ** 2))

    def get_edit_url(self):
        return reverse('portfolio', kwargs={'port_id': self.id})

    def efficient_frontier(self):
        tickers = [ticker.ticker for ticker in self.port_tickers.filter(is_sell=False)]
        assets = [ticker.ticker for ticker in tickers]

        df = pd.DataFrame()
        for ticker in assets:
            new_df = read_stock_data(ticker)
            df = new_df if df.empty else df.join(new_df, how="outer")

        log_returns = np.log(df / df.shift(1))
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
    timestamp = models.DateField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)
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
            self.qty = self.starting_investment / self.starting_value_of_ticker if self.starting_value_of_ticker != 0 else 0
            self.current_value_of_ticker = self.ticker.price
            self.current_value = Decimal(self.qty) * Decimal(self.current_value_of_ticker)
        else:
            self.close_value = self.current_value
        super().save(*args, **kwargs)
        self.portfolio.save()

    def tag_starting_price(self):
        return f"{round(self.starting_value_of_ticker, 2)} {CURRENCY}"

    def tag_current_price(self):
        return f"{round(self.current_value_of_ticker, 2)} {CURRENCY}"

    def tag_starting_value(self):
        return (f"{round(self.starting_investment, 2)} {CURRENCY}")

    def tag_current_value(self):
        return (f"{round(self.current_value, 2)} {CURRENCY}")

    def tag_diff_value(self):
        return f"{round(self.current_value - self.starting_investment, 2)} {CURRENCY}"

    def tag_diff_price(self):
        return f"{round(self.current_value_of_ticker - self.starting_value_of_ticker, 2)} {CURRENCY}"

    def tag_diff_pct(self):
        first_step = self.current_value / self.starting_investment
        first_step = first_step - 1
        return f"{round(first_step*100, 2)} %"


    def tag_ticker_title(self):
        return f"{self.ticker.title}"