import quantstats as qs
import yfinance as yf


aapl = yf.Ticker("AAPL").history(period="5y")
aapl.reset_index(inplace=True)
aapl.set_index("Date", inplace=True)
new_df = aapl[['Close']]
new_df["daily_return"] = new_df["Close"].pct_change().fillna(0)
print(new_df.head())