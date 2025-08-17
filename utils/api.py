# import requests
# import pandas as pd

# API_KEY = "RPMTB34B15HYCN4V"

# class AlphaVantageAPI:
#     @staticmethod
#     def get_intraday_data(symbol: str, interval: str = "1min", outputsize: str = "compact") -> pd.DataFrame:
#         url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={API_KEY}"
#         response = requests.get(url)
#         data = response.json()

#         key = f"Time Series ({interval})"
#         if key not in data:
#             raise ValueError(f"No time series data for {symbol}")

#         df = pd.DataFrame.from_dict(data[key], orient="index")
#         df.index = pd.to_datetime(df.index)
#         df = df.sort_index()
#         df.columns = [c.split(". ")[1] for c in df.columns]
#         df = df.apply(pd.to_numeric)
#         return df

# utils/api.py
import os
from typing import Optional
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY") 

class AlphaVantageAPI:
    @staticmethod
    def _check_api_key():
        if not API_KEY:
            raise RuntimeError("Alpha Vantage API key not configured. Set ALPHAVANTAGE_API_KEY.")

    @staticmethod
    def get_intraday_data(symbol: str, interval: str = "1min", outputsize: str = "compact") -> pd.DataFrame:
        AlphaVantageAPI._check_api_key()
        url = (
            f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={API_KEY}"
        )
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        key = f"Time Series ({interval})"
        if key not in data:
            # surface API error message if present
            raise ValueError(data.get("Note") or data.get("Error Message") or f"No time series data for {symbol}")

        df = pd.DataFrame.from_dict(data[key], orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df.columns = [c.split(". ")[1] for c in df.columns]
        df = df.apply(pd.to_numeric, errors="coerce")
        # standardize column names to lowercase
        df.columns = [c.lower().replace(" ", "_") for c in df.columns]
        return df

    @staticmethod
    def get_daily_adjusted(symbol: str, outputsize: str = "compact") -> pd.DataFrame:
        """
        Fetch TIME_SERIES_DAILY_ADJUSTED. Returns DataFrame indexed by date (UTC),
        columns: open, high, low, close, adjusted_close, volume, dividend_amount, split_coefficient
        """
        AlphaVantageAPI._check_api_key()
        url = (
            "https://www.alphavantage.co/query"
            f"?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}"
            f"&outputsize={outputsize}&apikey={API_KEY}"
        )
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        key = "Time Series (Daily)"
        if key not in data:
            raise ValueError(data.get("Note") or data.get("Error Message") or f"No daily data for {symbol}")

        df = pd.DataFrame.from_dict(data[key], orient="index")
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        # Map the verbose AV columns to normalized names
        col_map = {
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. adjusted close": "adjusted_close",
            "6. volume": "volume",
            "7. dividend amount": "dividend_amount",
            "8. split coefficient": "split_coefficient",
        }
        df = df.rename(columns=col_map)
        df = df.apply(pd.to_numeric, errors="coerce")
        return df