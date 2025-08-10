from django.db import models
from django.contrib.auth import get_user_model
import datetime
from datetime import timedelta
import pandas as pd
from tickers.helpers_folder.helpers import read_stock_data
from tickers.models import Ticker



User = get_user_model()


class TickerAnalysis(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.ticker.title

    def get_dataframe(self, days=360, is_updated=False):
        date_start = datetime.datetime.now() - timedelta(days=days)
        return read_stock_data(
            ticker=self.ticker.ticker,
            start=date_start,
            end=datetime.datetime.now().today(),
            updated=is_updated
        )

    def EMA(self, average_length: int = 50):
        """
            Exponential Moving Average
            Its better for trends cause give more weight on recent data
        """
        data = self.get_dataframe()
        return data.ewm(span=average_length, adjust=False).mean()
    

    def MACD(self, fast_period=12, slow_period=26, signal_period=9):
        """
            Moving Average Convergence Divergence
            Designed to capture short to medium-term trends in daily price data.
        
        """
        data = read_stock_data(self.ticker.ticker)

        ema_fast = data['Close'].ewm(span=fast_period, adjust=False).mean()
    
        # Calculate the long-term EMA
        ema_slow = data['Close'].ewm(span=slow_period, adjust=False).mean()

        # Calculate the MACD line
        macd = ema_fast - ema_slow
        
        # Calculate the signal line
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        
        # Calculate the MACD histogram
        histogram = macd - signal
        
        return macd, signal, histogram



    def generate_signals(self):
        buy_signals, sell_signals = [], []
        macd, signal, histogram = self.MACD()

        for i in range(1, len(macd)):
            if macd[i] > signal[i] and macd[i-1] <= signal[i-1]:
                buy_signals.append(i)
            elif macd[i] < signal[i] and macd[i-1] >= signal[i-1]:
                sell_signals.append(i)
    
        return buy_signals, sell_signals, histogram
    

    def calculate_historic_rsi(self, period=14):
        """
        Traditionally, RSI values of 70 or above indicate that an asset is becoming 
        overbought or overvalued, while an RSI of 30 or below suggests an oversold or 
        undervalued condition.
        """
        data = read_stock_data(self.ticker.ticker)
        close_delta = data["Close"].diff()

        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)


        # Calculate the EWMA
        ma_up = up.ewm(com = period - 1, adjust=True, min_periods = period).mean()
        ma_down = down.ewm(com = period - 1, adjust=True, min_periods = period).mean()
        
        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))
        
        return rsi
