import yfinance as yf
import pandas as pd

def fetch_asset_data(ticker, start=None, end=None, period='3y', interval='1d'):
    try:
        asset = yf.Ticker(ticker)
        if start and end:
            df = asset.history(start=start, end=end)
        else:
            df = asset.history(period=period, interval=interval)
        return df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def calculate_daily_returns(df):
    df = df.copy()
    df['Daily_Return'] = df['Close'].pct_change()
    return df

def clean_missing_data(df):
    return df.dropna(subset=['Daily_Return'])

def process_asset_data(df):
    df = calculate_daily_returns(df)
    df = clean_missing_data(df)
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1
    df['Predicted_Direction'] = df['Daily_Return'].apply(lambda x: 'Increase' if x > 0 else 'Decrease')
    return df