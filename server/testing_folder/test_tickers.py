import yfinance as yf
import numpy as np
import pandas as pd
import datetime


ticker = yf.Ticker("TSLA")
df = ticker.history(start="2010-01-01", end=datetime.datetime.now())

df["simply_return"] = df["Close"].pct_change()
print(df["simply_return"].mean() * 250)
