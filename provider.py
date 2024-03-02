from pandas_datareader import data as pdr
import yfinance as yf
import investpy as iv
import json

yf.pdr_override()

def get_major_forex_prices_from_yahoo(start="2003-01-01", end="2023-12-31", interval="1wk"):
    """Get by default weekly Major Forex Prices from 2003 to 2023 from Yahoo Finance"""
    majors = ['EURUSD=X', 'GBPUSD=X']
    data = pdr.get_data_yahoo(majors, start=start, end=end, interval=interval)
    return data

def get_major_forex_returns_from_yahoo(start="2003-01-01", end="2023-12-31", interval="1wk"):
    """Get by default weekly Major Forex Returns based on Close from 2003 to 2023 from Yahoo Finance"""
    majors = ["EURUSD=X", "GBPUSD=X", "NZDUSD=X", "USDCAD=X", "USDCHF=X", "USDJPY=X", "AUDUSD=X"]
    column_names = ["EURUSD", "GBPUSD", "NZDUSD", "USDCAD", "USDCHF", "USDJPY", "AUDUSD"]
    data = pdr.get_data_yahoo(majors, start=start, end=end, interval=interval)["Close"].pct_change().dropna()
    data.columns = column_names
    return data

def get_forex_returns_from_investdotcom(pair="EUR/USD", start="01/01/2023", end="01/01/2024", interval="Weekly"):
    """Get by default weekly Forex Prices from 2023 to 2024 from Investing.com"""
    data = iv.get_currency_cross_historical_data(currency_cross=pair, from_date=start, to_date=end, interval=interval)
    return data["Close"].pct_change().dropna()

def get_currency_pairs_metainformation(relativ_path = "./", file_name = "pairs.json"):
    """Load local JSON File with Currency Pairs Metainformation"""
    with open(relativ_path + file_name) as file:
        return json.load(file)
    
def make_pairs_list_from_metainformation(list_of_pairs_metainformation):
    """Make List of Currency Pairs from List of Metainformation about Currency Pairs for Investing.com"""
    return [pair["basis"]["currency"]["code"]["iso"] + pair["delimiter"]["investingdotcom"] + pair["counter"]["currency"]["code"]["iso"] for pair in list_of_pairs_metainformation]

def get_yield_code_basis_currency(currency, metainformation):
    """Get Yield Code for Investing.com for Basis Currency by ISO-Code from Metainformation"""
    return list(filter(lambda x: x["basis"]["currency"]["code"]["iso"] == currency, metainformation))[0]["basis"]["yield"]["code"]["investingdotcom"]

def get_yield_code_counter_currency(currency, metainformation):
    """Get Yield Code for Investing.com for Counter Currency by ISO-Code from Metainformation"""
    return list(filter(lambda x: x["counter"]["currency"]["code"]["iso"] == currency, metainformation))[0]["counter"]["yield"]["code"]["investingdotcom"]