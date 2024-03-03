from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import yfinance as yf
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

def get_currency_pairs_metainformation(relativ_path = "./", file_name = "pairs.json"):
    """Load local JSON File with Currency Pairs Metainformation"""
    with open(relativ_path + file_name) as file:
        return json.load(file)
    
def make_pairs_list_from_metainformation(list_of_pairs_metainformation):
    """Make List of Currency Pairs from List of Metainformation about Currency Pairs for Investing.com"""
    return [pair["basis"]["currency"]["code"]["iso"] + pair["delimiter"]["investingdotcom"] + pair["counter"]["currency"]["code"]["iso"] for pair in list_of_pairs_metainformation]

def get_yield_code_basis_currency(currency, metainformation):
    """Get Yield Code for Yahoo Finance for Basis Currency by ISO-Code from Metainformation"""
    return list(filter(lambda x: x["basis"]["currency"]["code"]["iso"] == currency, metainformation))[0]["basis"]["yield"]["code"]["yahoofiannce"]

def get_yield_code_counter_currency(currency, metainformation):
    """Get Yield Code for Yahoo Finance for Counter Currency by ISO-Code from Metainformation"""
    return list(filter(lambda x: x["counter"]["currency"]["code"]["iso"] == currency, metainformation))[0]["counter"]["yield"]["code"]["yahoofiannce"]

def get_yield_differential(pair, start="2013-01-01", end="2023-12-31", periods_per_year = 52):
    """Get Yield Differential between Basis and Counter Currency with Yields from local File for specific Periods per Year"""

    mapping = {"AUD": "AD",
               "CAD": "CA",
               "EUR": "EU",
               "JPY": "JP",
               "NZD": "NZ",
               "GBP": "UK",
               "USD": "US"}
    
    basis_currency = pair[:3]
    counter_currency = pair[3:]

    # r = (1+i)^(1/n)-1

    yield_data_basis = (1 + get_yield(mapping[basis_currency])) ** ( 1 / periods_per_year) - 1
    yield_data_counter = (1 + get_yield(mapping[counter_currency])) ** ( 1 / periods_per_year) - 1
    yield_data_differential = yield_data_basis - yield_data_counter
    return yield_data_basis, yield_data_counter, yield_data_differential

def wrangle_yield_files(relativ_path = "./Data/Yields/"):
    """Wrangle Yield Files from EconDB"""

    countrys = ["AU","CA","EU","JP","NZ","UK","US"]
    
    for country in countrys:
        file_name = f"EconDB {country} 3 Month Yield.csv"
        df = pd.read_csv(relativ_path + file_name, index_col=0, parse_dates=True)
        df.columns = ["Yield"]
        df = df.loc["2012-12-31":"2023",].resample('W').last().ffill()
        target_file = f"EconDB {country} 3 Month Yield 2013 to 2023 Weekly.csv"
        df.to_csv(relativ_path + target_file)

def get_yield(country, relativ_path="./Data/Yields/", file_format = "EconDB {country} 3 Month Yield 2013 to 2023 Weekly.csv"):
    """Get Yield Data from EconDB"""

    file_name = file_format.format(country=country)
    df = pd.read_csv(relativ_path + file_name, index_col=0, parse_dates=True)
    return df / 100