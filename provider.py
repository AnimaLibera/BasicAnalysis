from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

def get_major_forex_prices(start="2003-01-01", end="2023-12-31", interval="1wk"):
    """Get by default weekly Major Forex Prices from 2003 to 2023 from Yahoo Finance"""
    majors = ['EURUSD=X', 'GBPUSD=X']
    data = pdr.get_data_yahoo(majors, start=start, end=end, interval=interval)
    return data

def get_major_forex_returns(start="2003-01-01", end="2023-12-31", interval="1wk"):
    """Get by default weekly Major Forex Returns based on Close from 2003 to 2023 from Yahoo Finance"""
    majors = ["EURUSD=X", "GBPUSD=X", "NZDUSD=X", "USDCAD=X", "USDCHF=X", "USDJPY=X", "AUDUSD=X"]
    column_names = ["EURUSD", "GBPUSD", "NZDUSD", "USDCAD", "USDCHF", "USDJPY", "AUDUSD"]
    data = pdr.get_data_yahoo(majors, start=start, end=end, interval=interval)["Close"].pct_change().dropna()
    data.columns = column_names
    return data